import boto3
import os 

# Create a Boto3 session with credentials (not recommended for production)
session = boto3.Session()

# Create IAM client using the session
iam = session.client('iam')

# Specify the IAM user name
username = 'cloudAdmin'

# Get user details
response = iam.get_user(UserName=username)

# Print user information
user = response['User']
print("User Name     :", user['UserName'])
print("User ID       :", user['UserId'])
print("User ARN      :", user['Arn'])
print("Created On    :", user['CreateDate'])
