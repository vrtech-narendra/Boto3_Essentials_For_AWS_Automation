import argparse
import sys 
import csv
try: 
    import boto3
    from botocore.exceptions import (
            ProfileNotFound,
            NoRegionError,
            NoCredentialsError,
            PartialCredentialsError,
            EndpointConnectionError,
            WaiterError,
            ConnectTimeoutError,
            ReadTimeoutError,
            UnknownServiceError,
            ClientError

    )
except ModuleNotFoundError :
    print("Error : Please Install boto3 Module First and Retry")
    sys.exit(1)

try:
    parser = argparse.ArgumentParser(description="Get EC2 Discovery Script ")
    parser.add_argument('-p', '--profileName',required=True, help="AWS CLI Profile Name ")
    parser.add_argument('-r', '--region', required=True, help="EC2 Instance Region")
    
    args = parser.parse_args()
    profileName=args.profileName
    region=args.region   
    output_file='ec2Discovery.csv'
    print("Script Inputs are: ")
    print(f"    AWS CLI Profile : {profileName}")
    print(f"    region          : {region}")

    #Develop Python Boto3 Client Logic
    session = boto3.Session(profile_name=profileName)
    ec2Client = session.client(service_name='ec2', region_name=region)
    #Name: instance-state-name
    #Values: pending | running | shutting-down | terminated | stopping | stopped
    f1= {'Name': 'instance-state-name', 'Values': ['stopped'] }
    f2 = {'Name': 'instance-type', 'Values': ['t2.micro', 't2.nano']}
    f3= {'Name': 'availability-zone', 'Values': ['us-east-1c']}
    f4= {'Name': 'tag:projectname', 'Values': ['hr']}
    paginator = ec2Client.get_paginator('describe_instances')
    response_iterator = paginator.paginate(Filters=[f4])
    sno = 1
 
    for eachPage in response_iterator:
        for reservation in eachPage['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance.get('InstanceId', '')
                state = instance.get('State', {}).get('Name', '')
                print(f"{sno} InstanceId {instance_id} and State {state}")
                sno+=1
    if sno == 1:
        print(f'There are no EC2 Instances for your given filter')
except ProfileNotFound:
    print("Error : AWS CLI profile not found. Please check the profile name.")    
    sys.exit(1)
except NoRegionError:
    print("Error : AWS region not specified. Use --region or set it in your config.")
    sys.exit(1)
except NoCredentialsError:
    print("Error : AWS credentials not found. Please configure them using 'aws configure'.")
    sys.exit(1)
except PartialCredentialsError:
    print("Error : Incomplete credentials. Please provide both Access Key and Secret Key.")
    sys.exit(1)
except EndpointConnectionError:
    print("Error : Could not connect to AWS endpoint. Check your internet or region name.")
    sys.exit(1)
except ConnectTimeoutError:
    print("Error : Connection to AWS timed out while trying to establish connection.")
    sys.exit(1)
except ReadTimeoutError:
    print("Error : Connected, but AWS service didn't respond in time.")
    sys.exit(1)
except WaiterError as e:
    print(f"Error : Waiter error: {e}")
    sys.exit(1)
except UnknownServiceError as e:
    print(f"Error : UnknownServiceError: {e}. The service name might be incorrect or unsupported in this region.")
    sys.exit(1)
except AttributeError as e:
    print(f"Error : AttributeError : {e} ")
    sys.exit(1)
except ClientError as e:
    errorCode=e.response['Error']['Code']
    errorMessage=e.response['Error']['Message']
    print(f"AWS service Error -> code : {errorCode} and Message: {errorMessage}")
    sys.exit(1)
except Exception as e:
    print("Unexpected Error:", str(e))
    sys.exit(1)
