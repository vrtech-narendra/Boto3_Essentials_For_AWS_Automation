import sys 
import time
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
    parser.add_argument('-t', '--instacneType',required=True, help="EC2 Instance Type to update")        
    args = parser.parse_args()
    profileName=args.profileName
    regionName = args.regionName
    instanceId = args.instanceId
    instacneType=args.instacneType
    print(f"Inputs are: ")
    print(f"    AWS Profile : {profileName}")
    print(f"    Region Name : {regionName}")
    print(f"    Instance Id : {instanceId}")
    print(f"    instacneType: {instacneType}")

    session = boto3.Session(profile_name=profileName)
    ec2Client = session.client(service_name='ec2', region_name=regionName)

    response = ec2Client.describe_instances(  InstanceIds=[ instanceId ])
    instanceDetails = response.get('Reservations')[0].get('Instances')[0]
       
    currentInstanceType = instanceDetails.get("InstanceType")

    if currentInstanceType == instacneType:
        print(f"The required instance type is already matched")
        sys.exit(0)
    state = instanceDetails.get('State').get('Name') 
    if state == 'running':
        print(f"Stopping EC2 Instance...")
        response = ec2Client.stop_instances( InstanceIds=[ instanceId])
        waiter = ec2Client.get_waiter('instance_stopped')
        waiter.wait(  InstanceIds=[instanceId], WaiterConfig={ 'Delay': 5,'MaxAttempts': 60 })
        print(f"Stopped EC2 Instance")

    print(f"The current Instance Type for {instanceId} is {currentInstanceType}")
    print(f"Updating instance type to {instacneType}")
    response = ec2Client.modify_instance_attribute(InstanceId=instanceId,InstanceType={  'Value':  instacneType})
    print(f"The instance type has been updated to {instacneType}")
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
