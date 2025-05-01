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
        
        parser = argparse.ArgumentParser(description="Get All IAM Users with their UserIds")
        parser.add_argument('-p', '--profileName',required=True, help="AWS CLI Profile Name ")

        args = parser.parse_args()
        profileName=args.profileName

        #Develop Python boto3 logic for your requirement
        session = boto3.Session(profile_name=profileName)
        s3Resource = session.resource(service_name='s3')
        s3Client   = session.client(service_name='s3')

        #To List All S3 Buckets using resource
        # cnt=1
        # bucket_iterator = s3Resource.buckets.all()
        # for eachBucket in bucket_iterator:
        #     print(cnt,eachBucket.name)
        #     cnt+=1
        # if cnt == 1:
        #     print(f"There are no buckets under given AWS Profile/Account {profileName}")

        #To List All S3 Buckets using client
        paginator = s3Client.get_paginator('list_buckets')
        response_iterator = paginator.paginate()
        cnt=1
        for eachPage in response_iterator:
            for eachBucket in eachPage.get('Buckets'):
                print(cnt, eachBucket.get('Name'))
                cnt+=1
        if cnt == 1:
            print(f"There are no buckets under given AWS Profile/Account {profileName}")
       
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