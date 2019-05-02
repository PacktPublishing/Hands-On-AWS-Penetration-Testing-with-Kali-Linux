#!/usr/bin/env python3

import boto3
import json

session = boto3.session.Session(profile_name='Test', region_name='us-west-2')
client = session.client('s3')

bucket_names = []

response = client.list_buckets()
for bucket in response['Buckets']:
    bucket_names.append(bucket['Name'])

bucket_objects = {}

for bucket in bucket_names:
    response = client.list_objects_v2(Bucket=bucket, MaxKeys=1000)

    bucket_objects[bucket] = response['Contents']

    while response['IsTruncated']:
        response = client.list_objects_v2(Bucket=bucket, MaxKeys=1000, ContinuationToken=response['NextContinuationToken'])

        bucket_objects[bucket].extend(response['Contents'])

for bucket in bucket_names:
    with open('./{}.txt'.format(bucket), 'w+') as f:
        for bucket_object in bucket_objects[bucket]:
            f.write('{} ({} bytes)\n'.format(bucket_object['Key'], bucket_object['Size']))
