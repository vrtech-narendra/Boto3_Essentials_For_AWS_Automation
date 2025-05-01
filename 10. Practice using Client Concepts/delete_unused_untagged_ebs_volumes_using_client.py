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
        parser.add_argument('-r', '--regionName',required=True, help="Region name to work with ebs volumes ")
        args = parser.parse_args()
        profileName=args.profileName
        regionName = args.regionName

        #Develop Python boto3 logic for your requirement
        session = boto3.Session(profile_name=profileName)
        ec2Client = session.client(service_name='ec2', region_name=regionName)
        paginator = ec2Client.get_paginator('describe_volumes')
        f1={"Name": "status"   , "Values": ["available"]}
        response_iterator = paginator.paginate(Filters=[f1])
        cnt=1
        volumeIds=[]
        for eachPage in response_iterator:
            for eachVolume in eachPage.get('Volumes'):
                if not eachVolume.get('Tags') :
                    volumeId=eachVolume.get('VolumeId')
                    print(f"Deleting VolumeId {volumeId}....")
                    response = ec2Client.delete_volume(VolumeId=volumeId)
                    volumeIds.append(volumeId)
                    cnt+=1
        for eachVolumeId in volumeIds:
            print(f"Waiting to confirm volumeid {eachVolumeId} state as deleted...")
            waiter = ec2Client.get_waiter('volume_deleted')
            waiter.wait(VolumeIds=[ eachVolumeId ])
            print(f"The volumeid {eachVolumeId} has been delete")

        if cnt==1:
            print(f"There are no unused and untagged ebs volumes under given region {regionName}")        

       
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