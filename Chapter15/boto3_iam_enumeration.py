#!/usr/bin/env python3

import boto3
import json

session = boto3.session.Session(profile_name='Test', region_name='us-west-2')
client = session.client('iam')

user_details = []
group_details = []
role_details = []
policy_details = []

response = client.get_account_authorization_details()

if response.get('UserDetailList'):
    user_details.extend(response['UserDetailList'])
if response.get('GroupDetailList'):
    group_details.extend(response['GroupDetailList'])
if response.get('RoleDetailList'):
    role_details.extend(response['RoleDetailList'])
if response.get('Policies'):
    policy_details.extend(response['Policies'])

while response['IsTruncated']:
    response = client.get_account_authorization_details(Marker=response['Marker'])
    if response.get('UserDetailList'):
        user_details.extend(response['UserDetailList'])
    if response.get('GroupDetailList'):
        group_details.extend(response['GroupDetailList'])
    if response.get('RoleDetailList'):
        role_details.extend(response['RoleDetailList'])
    if response.get('Policies'):
        policy_details.extend(response['Policies'])

with open('./users.json', 'w+') as f:
    json.dump(user_details, f, indent=4, default=str)
with open('./groups.json', 'w+') as f:
    json.dump(group_details, f, indent=4, default=str)
with open('./roles.json', 'w+') as f:
    json.dump(role_details, f, indent=4, default=str)
with open('./policies.json', 'w+') as f:
    json.dump(policy_details, f, indent=4, default=str)
	
	
username = client.get_user()['User']['UserName'] 

current_user = None


for user in user_details:
    if user['UserName'] == username:
        current_user = user
       
        break

my_policies = []
if current_user.get('UserPolicyList'):
    for policy in current_user['UserPolicyList']:
	   my_policies.append(policy['PolicyDocument'])
	   
if current_user.get('AttachedManagedPolicies'):
   for managed_policy in user['AttachedManagedPolicies']:
      policy_arn = managed_policy['PolicyArn']
	  for policy_detail in policy_details:
	     if policy_detail['Arn'] == policy_arn:
		    default_version = policy_detail['DefaultVersionId']
			for version in policy_detail['PolicyVersionList']:
			   if version['VersionId'] == default_version:
			      my_policies.append(version['Document'])
				  break
			break
			
			
if current_user.get('GroupList'):
   for user_group in current_user['GroupList']:
      for group in group_details:
	      if group['GroupName'] == user_group:
		     if group.get('GroupPolicyList'):
			    for inline_policy in group['GroupPolicyList']:
				     my_policies.append(inline_policy['PolicyDocument'])
			 if group.get('AttachedManagedPolicies'):
			    for managed_policy in group['AttachedManagedPolicies']:
				   policy_arn = managed_policy['PolicyArn']
				   for policy in policy_details:
				      if policy['Arn'] == policy_arn:
					     default_version = policy['DefaultVersionId']
						 for version in policy['PolicyVersionList']:
						    if version['VersionId'] == default_version:
							   my_policies.append(version['Document'])
							   break
							break
		  

with open('./my-user-permissions.json', 'w+') as f:
    json.dump(my_policies, f, indent=4, default=str)