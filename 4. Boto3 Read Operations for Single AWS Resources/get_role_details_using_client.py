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
    parser = argparse.ArgumentParser(description="Get IAM Role Details ")
    parser.add_argument('-p', '--profileName',required=True, help="AWS CLI Profile Name ")    
    parser.add_argument('-r', '--roleName', required=True, help="IAM Role Name to get Details")
    args = parser.parse_args()
    profileName=args.profileName
    roleName=args.roleName

    session = boto3.Session(profile_name=profileName)
    iamClient = session.client(service_name='iam')

    response = iamClient.get_role(RoleName=roleName)
    roleDetails = response.get('Role')
    print(f"The IAM Role {roleName} Details are: ")
    print(f"RoleId     : {roleDetails.get('RoleId')}")
    print(f"RoleArn    : {roleDetails.get('Arn')}")
    print(f"CreatedAt  : {roleDetails.get('CreateDate')}")
    print(f"PermissionsBoundary: {roleDetails.get('PermissionsBoundary')}")

    
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