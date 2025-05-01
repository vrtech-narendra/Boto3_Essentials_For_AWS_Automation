import boto3

session = boto3.Session(profile_name='dev')
iamClient = session.client(service_name='iam')
ec2Client = session.client(service_name='ec2')

iamResource = session.resource(service_name='iam')
ec2Resource = session.resource(service_name='ec2')

print(f"Resource is available only for : { boto3.Session().get_available_resources()}")