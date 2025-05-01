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
        parser.add_argument('-r', '--region', required=True, help="EC2 Instance Region")
        parser.add_argument('-a', '--action', required=True, choices=['state', 'start', 'stop', 'terminate', 'reboot'], help='Action to execute on given ec2 instanceId')
        
        args = parser.parse_args()
        profileName=args.profileName
        region=args.region   
        action=args.action
    
        print("Script Inputs are: ")
        print(f"    AWS CLI Profile : {profileName}")
        print(f"    region          : {region}")
        print(f"    action          : {action}")


        #Develop Python Boto3 Logic
        session = boto3.Session(profile_name=profileName)
        ec2Client = session.client(service_name='ec2', region_name=region)
        paginator = ec2Client.get_paginator('describe_instances')
        f1={"Name": "tag:projectname", "Values": ['payments']}
        response_iterator = paginator.paginate(Filters=[f1])
        instanceIds=[]
        for eachPage in response_iterator:
            for eachReserveration in eachPage.get('Reservations'):
               for eachInstance in  eachReserveration.get('Instances'):
                  instanceIds.append(eachInstance.get('InstanceId'))
        
        if len(instanceIds) == 0:
            print(f"There are no instances under given region {region}")
            sys.exit()
        
        if action == 'state':
            for eachInstanceId in instanceIds:
                try:
                    print(f'Finding the instance {eachInstanceId} state...')
                    state = getEC2InstanceState(ec2Client,eachInstanceId)
                    print(f"The Current State of EC2 Instance {eachInstanceId} is {state}")
                except ClientError as e:
                    errorCode=e.response['Error']['Code']
                    if 'InvalidInstanceID' in errorCode:
                        print(f"The InstanceId {eachInstanceId} is {errorCode}")
                    else:
                        raise
        elif action == 'start':
            #First starting all instances
            startedInstancesId=[] #I will store into this only started instances because you dont need to wait for invalid ones when using waiter in second for loop
            for eachInstanceId in instanceIds:
                try:
                    print(f"Starting EC2 Instance {eachInstanceId}...")
                    state = getEC2InstanceState(ec2Client,eachInstanceId)
                    if state == "stopped":
                        response = ec2Client.start_instances( InstanceIds=[ eachInstanceId])
                        startedInstancesId.append(eachInstanceId)
                    else:
                        print(f"The current state of EC2 Instance {eachInstanceId} is {state} and no need to start/we can not execute start")
                except ClientError as e:
                    errorCode=e.response['Error']['Code']
                    if 'InvalidInstanceID' in errorCode:
                        print(f"The Instance Id {eachInstanceId} is {errorCode}")
                    else:
                        raise 
            #Now verifying the running status for all instances one by one 
            for eachInstanceId in startedInstancesId:
                try:
                    waiter = ec2Client.get_waiter('instance_running')
                    waiter.wait(  InstanceIds=[eachInstanceId])
                    print(f"The EC2 Instance {eachInstanceId} has been started")
                except WaiterError as e:
                    if 'InstanceRunning failed' in str(e):
                        print(f"Error : Waiter error: {str(e)} for InstanceId {eachInstanceId}")
                    else:
                        raise

        elif action == 'stop':
            #First Stopping all instances
            stoppedInstancesId=[] #I will store into this only started instances because you dont need to wait for invalid ones when using waiter in second for loop
            for eachInstanceId in instanceIds:
                try:
                    print(f"Stopping EC2 Instance {eachInstanceId}...")
                    state = getEC2InstanceState(ec2Client,eachInstanceId)
                    if state == "running":
                        response = ec2Client.stop_instances( InstanceIds=[ eachInstanceId])
                        stoppedInstancesId.append(eachInstanceId)
                    else:
                        print(f"The current state of EC2 Instance {eachInstanceId} is {state} and no need to stop/we can not execute stop")
                except ClientError as e:
                    errorCode=e.response['Error']['Code']
                    if 'InvalidInstanceID' in errorCode:
                        print(f"The Instance Id {eachInstanceId} is {errorCode}")
                    else:
                        raise 
            #Now verifying the running status for all instances one by one 
            for eachInstanceId in stoppedInstancesId:
                try:
                    waiter = ec2Client.get_waiter('instance_stopped')
                    waiter.wait(  InstanceIds=[eachInstanceId])
                    print(f"The EC2 Instance {eachInstanceId} has been stopped")
                except WaiterError as e:
                    if 'InstanceStopped failed' in str(e):
                        print(f"Error : Waiter error: {str(e)} for InstanceId {eachInstanceId}")
                    else:
                        raise

        elif action == 'reboot':
            #Here only one for loop to reboot instances an no need to use waiters for this action
            for eachInstanceId in instanceIds:
                try:
                    print(f"Rebooting EC2 Instance {eachInstanceId}...")
                    state = getEC2InstanceState(ec2Client,eachInstanceId)
                    if state == "running":
                        response = ec2Client.reboot_instances( InstanceIds=[ eachInstanceId])
                        print(f"The instance {eachInstanceId} has been rebooted")
                    else:
                        print(f"The current state of EC2 Instance {eachInstanceId} is {state} and no need to stop/we can not execute stop")
                except ClientError as e:
                    errorCode=e.response['Error']['Code']
                    if 'InvalidInstanceID' in errorCode:
                        print(f"The Instance Id {eachInstanceId} is {errorCode}")
                    else:
                        raise 

        elif action == 'terminate':
            #First Terminating all instances
            terminatedInstancesIds=[]
            for eachInstanceId in instanceIds:
                try:            
                    print(f"Terminating EC2 Instance {eachInstanceId}...")
                    state = getEC2InstanceState(ec2Client, eachInstanceId)
                    if state in ["running", "stopped"]:
                        response = ec2Client.terminate_instances(InstanceIds=[eachInstanceId])
                        terminatedInstancesIds.append(eachInstanceId)
                    else:
                        print(f"The current state of EC2 Instance {eachInstanceId} is {state} and termination is not applicable.")
                except ClientError as e:
                    errorCode=e.response['Error']['Code']
                    if 'InvalidInstanceID' in errorCode:
                        print(f"The Instance Id {eachInstanceId} is {errorCode}")
                    else:
                        raise 

            #Now verifying the terminate status for all instances one by one 
            for eachInstanceId in terminatedInstancesIds:
                try:
                    waiter = ec2Client.get_waiter('instance_terminated')
                    waiter.wait(  InstanceIds=[eachInstanceId])
                    print(f"The EC2 Instance {eachInstanceId} has been terminated")
                except WaiterError as e:
                    if 'InstanceTerminated failed' in str(e):
                        print(f"Error : Waiter error: {str(e)} for InstanceId {eachInstanceId}")
                    else:
                        raise

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