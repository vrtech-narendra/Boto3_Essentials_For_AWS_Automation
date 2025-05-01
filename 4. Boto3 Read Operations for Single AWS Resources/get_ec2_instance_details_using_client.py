import sys 
import argparse
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
    #Develop Python boto3 logic for your requirement
    parser = argparse.ArgumentParser(description="Get EC2 Instance Details ")
    parser.add_argument('-p', '--profileName',required=True, help="AWS CLI Profile Name ")
    parser.add_argument('-r', '--regionName',required=True, help="Region for required InstanceId")    
    parser.add_argument('-i', '--instanceId',required=True, help="EC2 Instance Id")        
    args = parser.parse_args()
    profileName=args.profileName
    regionName = args.regionName
    instanceId = args.instanceId
    print(f"Inputs are: ")
    print(f"    AWS Profile : {profileName}")
    print(f"    Region Name : {regionName}")
    print(f"    Instance Id : {instanceId}")

    session = boto3.Session(profile_name=profileName)
    ec2Client = session.client(service_name='ec2', region_name=regionName)

    response = ec2Client.describe_instances(  InstanceIds=[ instanceId ])
    instanceDetails = response.get('Reservations')[0].get('Instances')[0]

    print(f"The EC2 Instance {instanceId} Details are: ")
    print(f"architecture    : {instanceDetails.get('Architecture')}")
    print(f"image_id        : {instanceDetails.get('ImageId')}")
    print(f"key_name        : {instanceDetails.get('KeyName')}")
    print(f"launch_time     : {instanceDetails.get('LaunchTime')}")
    print(f"platform        : {instanceDetails.get('PlatformDetails')}")
    print(f"public_ip_address   : {instanceDetails.get('PublicIpAddress')}")
    print(f"Current State   : {instanceDetails.get('State').get('Name')}")

    
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