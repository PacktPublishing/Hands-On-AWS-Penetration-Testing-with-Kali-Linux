import json
import boto3
def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    reservations = ec2.describe_instances()['Reservations']
    print(json.dumps(reservations, indent=2, default=str))