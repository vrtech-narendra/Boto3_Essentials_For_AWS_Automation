import boto3

# Create a Boto3 session with credentials (not recommended for production)
session = boto3.Session(
    aws_access_key_id='xxxxxxxxxxxxxx',
    aws_secret_access_key='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
    region_name='us-east-1'  # Change to your preferred region
)

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
