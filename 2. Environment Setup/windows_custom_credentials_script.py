import boto3
import configparser

# Load custom credentials from file
config = configparser.ConfigParser()
config.read('aws_credentials.ini')  # File path to your custom credentials

# Choose the profile you want to use
profile = 'dev'

# Read credentials
access_key = config[profile]['aws_access_key_id']
secret_key = config[profile]['aws_secret_access_key']
region = config[profile].get('region', 'us-east-1')

# Create a session with the custom credentials
session = boto3.Session(
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name=region
)

# Use the session
iam = session.client('iam')

username = 'cloudAdmin'
# Example: Get a specific user
response = iam.get_user(UserName=username)
user = response['User']
print("User Name     :", user['UserName'])
print("User ID       :", user['UserId'])
print("User ARN      :", user['Arn'])
print("Created On    :", user['CreateDate'])
