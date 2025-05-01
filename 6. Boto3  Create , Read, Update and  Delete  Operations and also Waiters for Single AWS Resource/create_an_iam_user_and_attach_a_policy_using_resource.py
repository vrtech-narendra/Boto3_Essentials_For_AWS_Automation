import sys 
import argparse
import time
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
        parser = argparse.ArgumentParser(description="Create an IAM User ")
        parser.add_argument('-p', '--profileName',required=True, help="AWS CLI Profile Name ")
        parser.add_argument('-u', '--userName', required=True, help="IAM User to Create")
        args = parser.parse_args()
        profileName=args.profileName
        userName=args.userName   
        policyArn = 'arn:aws:iam::aws:policy/AmazonEC2FullAccess'
        print(f"Inputs are: ")
        print(f"    Profile Name: {profileName}")
        print(f"    IAM User    : {userName}")
        print(f"    Policy ARN  : {policyArn}")

        session = boto3.Session(profile_name=profileName)
        iamResource = session.resource(service_name='iam')
        # iamClient = session.client(service_name='iam')

        print(f"Creating user object...")
        userObj = iamResource.User(userName)
        print(f"Creating user...")
        try:
            userObj = userObj.create()
            # waiter=iamClient.get_waiter('user_exists')
            waiter=iamResource.meta.client.get_waiter('user_exists')
            waiter.wait(UserName=userName)
        except ClientError as e:
            errorCode=e.response['Error']['Code']
            if errorCode == 'EntityAlreadyExists':
                print(f"Already IAM User is existing")
            else:
                raise

        print(f"Attaching a policy to user...")
        response = userObj.attach_policy( PolicyArn=policyArn)
        time.sleep(1)

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