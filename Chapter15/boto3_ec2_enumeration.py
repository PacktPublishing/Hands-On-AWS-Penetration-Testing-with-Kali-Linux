#!/usr/bin/env python3

import boto3
import json

session = boto3.session.Session(profile_name='Test', region_name='us-west-2')
client = session.client('ec2')

instances = []

response = client.describe_instances(MaxResults=1000)

for reservation in response['Reservations']:
    if reservation.get('Instances'):
        instances.extend(reservation['Instances'])

while response.get('NextToken'):
    response = client.describe_instances(MaxResults=1000, NextToken=response['NextToken'])

    for reservation in response['Reservations']:
        if reservation.get('Instances'):
            instances.extend(reservation['Instances'])

with open('./ec2-instances.json', 'w+') as f:
    json.dump(instances, f, indent=4, default=str)