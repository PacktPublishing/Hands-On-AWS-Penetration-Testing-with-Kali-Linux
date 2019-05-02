#!/usr/bin/env python3

# Import the necessary libraries
import argparse
from botocore.exceptions import ClientError

# Declare the required module info for the Pacu UI
module_info = {
    'name': 's3__enum',
    'author': 'Example author of Example company',
    'category': 'ENUM',
    'one_liner': 'Enumerates S3 buckets in the target account.',
    'description': 'This module enumerates what S3 buckets exist in the target account and saves the information to the Pacu database.',
    'services': ['S3'],
    'prerequisite_modules': [],
    'external_dependencies': [],
    'arguments_to_autocomplete': [],
}

# Define our argument parser, for if our module supported any arguments
parser = argparse.ArgumentParser(add_help=False, description=module_info['description'])

# Begin the main function, which is run when the module itself is run
def main(args, pacu_main):
    # Setup our session, arguments, and override the print function
    session = pacu_main.get_active_session()
    args = parser.parse_args(args)
    print = pacu_main.print

    # Create a variable to store data in as we enumerate it
    data = {'Buckets': []}

    # Attempt to list the buckets in the target account, catching any potential errors
    try:
        client = pacu_main.get_boto3_client('s3')

        data['Buckets'] = client.list_buckets()['Buckets']
    except ClientError as error:
        print('Failed to list S3 buckets: {}'.format(error))

    # Update the Pacu database with the S3 data that we enumerated
    session.update(pacu_main.database, S3=data)

    return data

# Define our summary function that outputs a short summary of the module execution after it is done
def summary(data, pacu_main):
    return 'Found {} S3 bucket(s).'.format(len(data['Buckets']))