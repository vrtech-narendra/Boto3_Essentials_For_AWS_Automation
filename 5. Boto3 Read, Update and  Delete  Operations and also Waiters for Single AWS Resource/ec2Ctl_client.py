import argparse
import time
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
def getEC2InstanceState(ec2Client,instanceId):
    response = ec2Client.describe_instances(  InstanceIds=[ instanceId ])
    instanceDetails = response.get('Reservations')[0].get('Instances')[0]
    state = instanceDetails.get('State').get('Name')    
    return state 

def main():
    try:
        parser = argparse.ArgumentParser(description="EC2 Instance State Management Control Script")
        parser.add_argument('-p', '--profileName',required=True, help="AWS CLI Profile Name ")
        parser.add_argument('-i', '--instanceId',required=True, help="Instance Id")
        parser.add_argument('-r', '--region', required=True, help="EC2 Instance Region")
        parser.add_argument('-a', '--action', required=True, choices=['state', 'start', 'stop', 'terminate', 'reboot'], help='Action to execute on given ec2 instanceId')
        
        args = parser.parse_args()
        profileName=args.profileName
        instanceId=args.instanceId
        region=args.region   
        action=args.action
    
        print("Script Inputs are: ")
        print(f"    AWS CLI Profile : {profileName}")
        print(f"    instanceId      : {instanceId}")
        print(f"    region          : {region}")
        print(f"    action          : {action}")
        print(f"Executing an action {action} on EC2 Instance {instanceId}...\n")

        #Develop Python Boto3 Logic
        session = boto3.Session(profile_name=profileName)
        ec2Client = session.client(service_name='ec2', region_name=region)


        if action == 'state':
            print(f'Finding the instance {instanceId} state...')
            state = getEC2InstanceState(ec2Client,instanceId)
            print(f"The Current State of EC2 Instance {instanceId} is {state}")
        elif action == 'start':
            print(f"Starting EC2 Instance {instanceId}...")
            state = getEC2InstanceState(ec2Client,instanceId)
            if state == "stopped":
                response = ec2Client.start_instances( InstanceIds=[ instanceId])
                waiter = ec2Client.get_waiter('instance_running')
                waiter.wait(  InstanceIds=[instanceId])
                print(f"The EC2 Instance {instanceId} has been started")
            else:
                print(f"The currrent state of EC2 Instance is {state} and no need to start/we can not start")
        

        elif action == 'stop':
            print(f"Stopping EC2 Instance {instanceId}...")
            state = getEC2InstanceState(ec2Client,instanceId)
            if state == "running":
                response = ec2Client.stop_instances( InstanceIds=[ instanceId])
                waiter = ec2Client.get_waiter('instance_stopped')
                waiter.wait(  InstanceIds=[instanceId], WaiterConfig={ 'Delay': 5,'MaxAttempts': 60 })
                print(f"The EC2 Instance {instanceId} has been stopped")
            else:
                print(f"The currrent state of EC2 Instance is {state} and no need to start/we can not start")
        
        elif action == 'reboot':
            print(f"Rebooting EC2 Instance {instanceId}...")
            state = getEC2InstanceState(ec2Client, instanceId)
            if state == "running":
                response = ec2Client.reboot_instances(InstanceIds=[instanceId])
                print(f"The EC2 Instance {instanceId} is rebooting now.")
            else:
                print(f"The current state of EC2 Instance is {state} and it must be in 'running' state to reboot.")

        elif action == 'terminate':
            print(f"Terminating EC2 Instance {instanceId}...")
            state = getEC2InstanceState(ec2Client, instanceId)
            if state in ["running", "stopped"]:
                response = ec2Client.terminate_instances(InstanceIds=[instanceId])
                waiter = ec2Client.get_waiter('instance_terminated')
                waiter.wait(InstanceIds=[instanceId], WaiterConfig={'Delay': 5, 'MaxAttempts': 60})
                print(f"The EC2 Instance {instanceId} has been terminated.")
            else:
                print(f"The current state of EC2 Instance is {state} and termination is not applicable.")

        
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
    
    return None


if __name__ == "__main__":
    main()