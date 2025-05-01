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
        parser = argparse.ArgumentParser(description="Launch EC2 Instance")
        parser.add_argument('-p', '--profileName',required=True, help="AWS CLI Profile Name ")
        parser.add_argument('-r', '--region', required=True, help="Region to provision an EC2 Instnace")
        args = parser.parse_args()
        profileName=args.profileName
        region=args.region   

        # Configuration
        region = region
        tag_key = 'projectName'
        tag_value='payments'
        ami_id = 'ami-0e449927258d45bc4'
        instance_type = 't2.micro'
        key_name = 'vrtech'
        security_group_id = 'sg-086a82403842f3025'      
        print(f"Inputs are: ")
        print(f"Region          : {region}")
        print(f"ami_id          : {ami_id}")
        print(f"instance_type   : {instance_type}")
        print(f"key_name        : {key_name}")
        print(f"Tag Key         : {tag_key}")
        print(f"Tag Value       : {tag_value}")
        print(f"Security Group ID : {security_group_id}")
    
        #Develop Python Boto3 Client Logic
        session = boto3.Session(profile_name=profileName)
        ec2Resource = session.resource(service_name='ec2', region_name=region)
        print(f"Launching EC2 Instance...")
        response = ec2Resource.create_instances(
                ImageId=ami_id,
                KeyName=key_name,
                InstanceType=instance_type,
                TagSpecifications=[
                    {
                        'ResourceType': 'instance',
                        'Tags': [
                            {
                                'Key': tag_key,
                                'Value': tag_value,
                            }
                        ]
                    }
                ],
                SecurityGroupIds=[security_group_id],
                MaxCount=1,
                MinCount=1

        )

        instanceObj=response[0]
        instanceId=instanceObj.id
        print(f"Wating..... to get EC2 Instance {instanceId} into running state...")
        instanceObj.wait_until_running()
        instanceObj.reload()
        publicIp=instanceObj.public_ip_address
        print(f"The Launched EC2 Instance {instanceId} and Its PublicIpAddress is {publicIp}")



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