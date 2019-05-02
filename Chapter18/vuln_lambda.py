import boto3
import subprocess
import urllib


def lambda_handler(event, context):
    try:
        s3 = boto3.client('s3')
        print(s3.list_buckets())
    except:
        pass

    s3 = boto3.client('s3')

    for record in event['Records']:
        try:
            bucket_name = record['s3']['bucket']['name']
            object_key = record['s3']['object']['key']
            object_key = urllib.parse.unquote_plus(object_key)

            if object_key[-4:] != '.zip':
                print('Not a zip file, not tagging')
                continue

            response = s3.get_object(
                Bucket=bucket_name,
                Key=object_key
            )

            file_download_path = f'/tmp/{object_key.split("/")[-1]}'
            with open(file_download_path, 'wb+') as file:
                file.write(response['Body'].read())

            file_count = subprocess.check_output(
                f'zipinfo {file_download_path} | grep ^- | wc -l',
                shell=True,
                stderr=subprocess.STDOUT
            ).decode().rstrip()
            s3.put_object_tagging(
                Bucket=bucket_name,
                Key=object_key,
                Tagging={
                    'TagSet': [
                        {
                            'Key': 'NumOfFilesInZip',
                            'Value': file_count
                        }
                    ]
                }
            )
        except Exception as e:
            print(f'Error on object {object_key} in bucket {bucket_name}: {e}')
    return