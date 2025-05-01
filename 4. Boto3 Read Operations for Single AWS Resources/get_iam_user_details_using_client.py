import boto3

session = boto3.Session(profile_name='dev')
iamClient = session.client(service_name='iam')

response = iamClient.get_user( UserName='cloudAdmin')
userDetails = response.get('User')
print(f"The details for the IAM User cloudAdmin are:")
print(f"UserName    : {userDetails.get('UserName')}")
print(f"UserId      : {userDetails.get('UserId')}")
print(f"UserArn     : {userDetails.get('Arn')}")
print(f"CreatedAt   : {userDetails.get('CreateDate')}")
