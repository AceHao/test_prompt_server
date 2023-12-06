import subprocess
import flask
import logging
from flask import Flask,jsonify
from os.path import exists
import iperf3
from multiprocessing import Process
import os
import boto3

# prompt server

app = Flask(__name__)

@app.route('/invocations', methods=['POST'])
def serve():
    return jsonify({"ExitCode": 0, "Body": "{}"})

def make_me_available():
    '''
    Implements a very simple method to mark an idle prompt server ready to take traffic.
    TODO: a prod-ready example for idle ip writing, based on dynamoDB, will be provided in next iteration.
    '''
    assigned_ip = os.environ['SM_ASSIGNED_PRIVATE_IP_REV_2023_10']
    if assigned_ip and len(assigned_ip) > 0:
        table_name = os.environ['ROUTING_TABLE_NAME']
        ddb_entry_key = os.environ['ROUTING_ENTRY_KEY']
        dynamodb = boto3.client('dynamodb', region_name='us-west-2')
        logging.info("Saving Table: {}, EndpointName: {}, IP: {}".format(table_name, ddb_entry_key, assigned_ip))
        dynamodb.update_item(
            TableName=table_name,
            Key={'EndpointName': {'S': ddb_entry_key}},
            UpdateExpression="SET #IP= :one".format(assigned_ip),
            ExpressionAttributeNames={"#IP": "{}".format(assigned_ip)},
            ExpressionAttributeValues={":one": {'N': '1'}}
        )

@app.route('/ping', methods=['GET'])
def ping():
    '''
    The standard API required for Sagemaker model container.
    When endpoint is InService, the platform will keep calling this API, which effectively means
    the IP assigned to this container will always shwon as available.
    TODO: in a production setting, make_me_available() shoud be called upon server startup, and
    after finish processing a prompt.
    '''
    make_me_available()
    return "success", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    
