import boto3 

session=boto3.Session(profile_name='dev')

ec2Client=session.client(service_name='ec2')
ec2Resource=session.resource(service_name='ec2')

# print(dir(ec2Resource))

# print(ec2Client.meta.region_name)
# print(ec2Client.meta.endpoint_url)
# print(ec2Client.meta.service_model.service_name)
# # print(dir(ec2Client.meta.service_model))
# print(dir(ec2Resource.meta))
print(ec2Resource.meta.service_name)
print(ec2Resource.meta.client.meta.region_name)
print(ec2Resource.meta.client.meta)