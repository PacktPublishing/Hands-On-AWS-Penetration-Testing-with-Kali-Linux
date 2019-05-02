import random

import boto3
import botocore


# A list of user agents that won't trigger GuardDuty
safe_user_agents = [
    'Boto3/1.7.48 Python/3.7.0 Windows/10 Botocore/1.10.48',
    'aws-sdk-go/1.4.22 (go1.7.4; linux; amd64)',
    'aws-cli/1.15.10 Python/2.7.9 Windows/8 botocore/1.10.10'
]

# Grab the current user agent
user_agent = boto3.session.Session()._session.user_agent().lower()

# Check if we are on Kali, Parrot, or Pentoo Linux against a lowercase version of the user agent
if 'kali' in user_agent.lower() or 'parrot' in user_agent.lower() or 'pentoo' in user_agent.lower():
    # Change the user agent to a random one from the list of safe user agents
    user_agent = random.choice(safe_user_agents)

# Prepare a botocore config object with our user agent
botocore_config = botocore.config.Config(
    user_agent=user_agent
)

# Create the boto3 client, using the botocore config we just set up
client = boto3.client(
    'ec2',
    region_name='us-east-1',
    config=botocore_config
)

# Print out the results of our EC2 DescribeInstances call
print(client.describe_instances())