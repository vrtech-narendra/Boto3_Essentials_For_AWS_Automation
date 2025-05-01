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
        parser.add_argument('-b', '--bucketName',required=True, help="Bucket Name to list object ")

        args = parser.parse_args()
        profileName=args.profileName
        bucketName=args.bucketName
        #Requirement: List Objects for a given Bucket and Download or Delete an Object

        session = boto3.Session(profile_name=profileName)
        s3Resource = session.resource(service_name='s3')

        bucket = s3Resource.Bucket(bucketName)
        object_summary_iterator = bucket.objects.filter(Prefix='configs/')
        cnt=1
        for eachBucketObject in object_summary_iterator:
            if eachBucketObject.key == 'configs/':
                continue
            print(cnt, eachBucketObject.key)
            cnt+=1
        if cnt == 1:
            print(f"There are no objects for a given bucket {bucketName}: ")
            return False 
        userChoice = input(f"Enter your choice - download/delete an object from {bucketName} ")
        if userChoice == "download":
            objectName = input("Enter your object to download: ")
            object = s3Resource.Object(bucketName,objectName)
            print(f"Downloding the s3 object {objectName} into .... current location")
            object.download_file('downloaded_object')
        elif userChoice == "delete":
            objectName = input("Enter your object to delete: ")
            object = s3Resource.Object(bucketName,objectName)
            print(f"Deleting object {object} from bucket {bucketName}...")
            response = object.delete()
            # print(response)
            print(f"Delete the object {object} from bucket {bucketName}")
        else:
            print(f"Invalid Choice . Please try again")
            return False

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