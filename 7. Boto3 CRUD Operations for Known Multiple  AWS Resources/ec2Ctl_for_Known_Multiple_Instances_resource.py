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

def main():
    try:
        parser = argparse.ArgumentParser(description="EC2 Instance State Management Control Script")
        parser.add_argument('-p', '--profileName',required=True, help="AWS CLI Profile Name ")
        parser.add_argument('-i', '--instanceIds',required=True, help="Instance Ids with comma separated values")
        parser.add_argument('-r', '--region', required=True, help="EC2 Instance Region")
        parser.add_argument('-a', '--action', required=True, choices=['state', 'start', 'stop', 'terminate', 'reboot'], help='Action to execute on given ec2 instanceId')
        
        args = parser.parse_args()
        profileName=args.profileName
        instanceIds=args.instanceIds.split(',')
        region=args.region   
        action=args.action
    
        print("Script Inputs are: ")
        print(f"    AWS CLI Profile : {profileName}")
        print(f"    instanceId      : {instanceIds}")
        print(f"    region          : {region}")
        print(f"    action          : {action}")
        print(f"Executing an action {action} on EC2 Instance {instanceIds}...\n")

        #Develop Python Boto3 Logic
        session = boto3.Session(profile_name=profileName)
        ec2Resource = session.resource(service_name='ec2', region_name=region)

        if action == 'state':
            for eachInstanceId in instanceIds:
                try:
                    instanceObj = ec2Resource.Instance(eachInstanceId)
                    print(f'Finding the instance {eachInstanceId} state...')
                    state = instanceObj.state.get('Name')
                    print(f"The current state of EC2 Instance {eachInstanceId} is {state}")
                except ClientError as e:
                    errorCode=e.response['Error']['Code']
                    if 'InvalidInstanceID' in errorCode:
                        print(f"The Instance Id {eachInstanceId} is {errorCode}")
                    else:
                        raise 
        elif action == 'start':
            #First starting all instances
            startedInstanceIds=[] #I will append into this only started instances because you dont need to wait for invalid ones when using waiter in second for loop
            for eachInstanceId in instanceIds:
                try:
                    instanceObj = ec2Resource.Instance(eachInstanceId)
                    print(f"Starting EC2 Instance {eachInstanceId}...")
                    state = instanceObj.state.get('Name')
                    if state == 'stopped':
                        start_reponse=instanceObj.start()
                        startedInstanceIds.append(eachInstanceId)
                    else:
                        print(f"The current state of EC2 Instance {eachInstanceId} is {state} and no need to start/we can not execute start")
                except ClientError as e:
                    errorCode=e.response['Error']['Code']
                    if 'InvalidInstanceID' in errorCode:
                        print(f"The Instance Id {eachInstanceId} is {errorCode}")
                    else:
                        raise 
            #Now verifying the running status for all instances one by one 
            for eachInstanceId in startedInstanceIds:
                try:
                    instanceObj = ec2Resource.Instance(eachInstanceId)
                    instanceObj.wait_until_running()
                    print(f"The EC2 Instance {eachInstanceId} has been started")
                except WaiterError as e:
                    if 'InstanceRunning failed' in str(e):
                        print(f"Error : Waiter error: {str(e)} for InstanceId {eachInstanceId}")
                    else:
                        raise

        elif action == 'stop':
            #First stopping all instances
            stoppedInstanceIds=[] #I will append into this only stopped instances because you dont need to wait for invalid ones when using waiter in second for loop
            for eachInstanceId in instanceIds:
                try:
                    instanceObj = ec2Resource.Instance(eachInstanceId)
                    print(f"Stopping EC2 Instance {eachInstanceId}...")
                    state = instanceObj.state.get('Name')
                    if state == 'running':
                        stop_reponse=instanceObj.stop()
                        stoppedInstanceIds.append(eachInstanceId)
                    else:
                        print(f"The current state of EC2 Instance {eachInstanceId} is {state} and no need to stop/we can not execute stop")
                except ClientError as e:
                    errorCode=e.response['Error']['Code']
                    if 'InvalidInstanceID' in errorCode:
                        print(f"The Instance Id {eachInstanceId} is {errorCode}")
                    else:
                        raise 
            #Now verifying the stopped status for all instances one by one 
            for eachInstanceId in stoppedInstanceIds:
                try:
                    instanceObj = ec2Resource.Instance(eachInstanceId)
                    instanceObj.wait_until_stopped()
                    print(f"The EC2 Instance {eachInstanceId} has been stopped")
                except WaiterError as e:
                    if 'InstanceStopped failed' in str(e):
                        print(f"Error : Waiter error: {str(e)} for InstanceId {eachInstanceId}")
                    else:
                        raise

        elif action == 'reboot':
            #Rebooting instances and no need of waiters here
            for eachInstanceId in instanceIds:
                try:
                    instanceObj = ec2Resource.Instance(eachInstanceId)
                    print(f"Rebooting EC2 Instance {eachInstanceId}...")
                    state = instanceObj.state.get('Name')
                    if state == 'running':
                        reboot_response = instanceObj.reboot()
                    else:
                        print(f"The current state of EC2 Instance {eachInstanceId} is {state} and no need to rebootop/we can not execute reboot")
                except ClientError as e:
                    errorCode=e.response['Error']['Code']
                    if 'InvalidInstanceID' in errorCode:
                        print(f"The Instance Id {eachInstanceId} is {errorCode}")
                    else:
                        raise                         
        elif action == 'terminate':
            #Terminating instances
            terminatedInstanceIds=[]
            for eachInstanceId in instanceIds:
                try:
                    instanceObj = ec2Resource.Instance(eachInstanceId)
                    print(f"Terminating EC2 Instance {eachInstanceId}...")
                    state = instanceObj.state.get('Name')            
                    state = instanceObj.state.get('Name')
                    if state in ['running', 'stopped']:
                        terminate_response = instanceObj.terminate()
                        terminatedInstanceIds.append(eachInstanceId)
                    else:
                        print(f"The current state of EC2 Instance {eachInstanceId} is {state}. Terminate operation not applicable.")
                except ClientError as e:
                    errorCode=e.response['Error']['Code']
                    if 'InvalidInstanceID' in errorCode:
                        print(f"The Instance Id {eachInstanceId} is {errorCode}")
                    else:
                        raise     
            #Now verifying the terminated status for all instances one by one 
            for eachInstanceId in terminatedInstanceIds:
                try:
                    instanceObj = ec2Resource.Instance(eachInstanceId)
                    instanceObj.wait_until_terminated()
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