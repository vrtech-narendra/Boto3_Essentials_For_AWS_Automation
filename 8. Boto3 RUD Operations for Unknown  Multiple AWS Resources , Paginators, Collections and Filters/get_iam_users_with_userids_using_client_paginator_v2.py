import argparse
import sys 
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
    parser = argparse.ArgumentParser(description="Get All IAM Users with their UserIds")
    parser.add_argument('-p', '--profileName',required=True, help="AWS CLI Profile Name ")

    args = parser.parse_args()
    profileName=args.profileName
  
    print("Script Inputs are: ")
    print(f"    AWS CLI Profile: {profileName}")


    session = boto3.Session(profile_name=profileName)
    iamClient = session.client(service_name='iam')
    responses=[]
    response = iamClient.list_users( MaxItems=1000)
    responses.append(response)
    Marker = response.get('Marker')
    
    while Marker:
        response = iamClient.list_users( MaxItems=1000, Marker=Marker)
        responses.append(response)
        Marker = response.get('Marker')        
    
    cnt=1
    for eachPage in responses:
        for eachIamUser in eachPage.get('Users'):
            print(f"{cnt} UserName: {eachIamUser.get('UserName')}") #UserId: {eachIamUser.get('UserId')} Arn: {eachIamUser.get('Arn')} CreatedAt: {eachIamUser.get('CreateDate')}")
            cnt+=1

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
