import boto3
import os 

# Create a Boto3 session with credentials (not recommended for production)
session = boto3.Session(
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
    region_name=os.environ.get('AWS_DEFAULT_REGION') # Change to your preferred region
)

# Create IAM client using the session

iamClient = session.client(service_name='iam')


# Specify the IAM user name
username = 'cloudAdmin'

# Get user details
response = iamClient.get_user(UserName=username)

# Print user information
user = response['User']
print("User Name     :", user['UserName'])
print("User ID       :", user['UserId'])
print("User ARN      :", user['Arn'])
print("Created On    :", user['CreateDate'])
