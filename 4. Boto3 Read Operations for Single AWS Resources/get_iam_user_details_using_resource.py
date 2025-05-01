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
    print("Please Install boto3 Module First and Retry")
    sys.exit(1)

def main():
    try:
        #Develop Python boto3 logic for your requirement
        parser = argparse.ArgumentParser(description="Get IAM User Details ")
        parser.add_argument('-p', '--profileName',required=True, help="AWS CLI Profile Name ")
        parser.add_argument('-u', '--userName', required=True, help="IAM User Name to get Details")

        args = parser.parse_args()
        profileName=args.profileName
        userName=args.userName 

        session = boto3.Session(profile_name=profileName)
        iamResource = session.resource(service_name='iam')
        userObj = iamResource.User(userName)

        print(f"The details for the IAM User {userName} are:")
        print(f"UserName    : {userObj.user_name}")
        print(f"UserId      : {userObj.user_id}")
        print(f"UserArn     : {userObj.arn}")
        print(f"CreatedAt   : {userObj.create_date}")        
        
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
        print(f"Error : AWS service Error -> code : {errorCode} and Message: {errorMessage}")
        sys.exit(1)
    except Exception as e:
        print("Error : Unexpected Error:", str(e))
        sys.exit(1)
    return None 

if __name__ == "__main__":
    main()