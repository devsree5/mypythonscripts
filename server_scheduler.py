import boto3
import datetime

def lambda_handler(event, context):
    # Define the EC2 instance ID
    instance_id = ''instance id = i-12xxxxx''
    
    # Define the EC2 client
    ec2_client = boto3.client('ec2')
    
    # Get the current time
    current_time = datetime.datetime.now().time()
    
    # Get the current day of the week (Monday is 0 and Sunday is 6)
    current_day = datetime.datetime.now().weekday()
    
    # Define the stop and start schedules
    stop_schedule = {
        'hour': 19,  # Stop at 7 PM
        'minute': 0,
        'second': 0
    }
    start_schedule = {
        'hour': 9,  # Start at 9 AM
        'minute': 0,
        'second': 0
    }
    
    # Check if it's Saturday or Sunday
    if current_day == 5 or current_day == 6:
        # Stop the instance if it's running
        stop_instance(ec2_client, instance_id)
    else:
        # Check if it's time to stop the instance
        if (
            current_time.hour == stop_schedule['hour'] and
            current_time.minute == stop_schedule['minute'] and
            current_time.second == stop_schedule['second']
        ):
            # Stop the instance if it's running
            stop_instance(ec2_client, instance_id)
        
        # Check if it's time to start the instance
        if (
            current_time.hour == start_schedule['hour'] and
            current_time.minute == start_schedule['minute'] and
            current_time.second == start_schedule['second']
        ):
            # Start the instance if it's stopped
            start_instance(ec2_client, instance_id)

def stop_instance(ec2_client, instance_id):
    # Check if the instance is already stopped
    response = ec2_client.describe_instances(InstanceIds=[instance_id])
    state = response['Reservations'][0]['Instances'][0]['State']['Name']
    if state == 'stopped':
        print(f"Instance {instance_id} is already stopped.")
        return
    
    # Stop the instance
    ec2_client.stop_instances(InstanceIds=[instance_id])
    print(f"Stopping instance {instance_id}.")

def start_instance(ec2_client, instance_id):
    # Check if the instance is already running
    response = ec2_client.describe_instances(InstanceIds=[instance_id])
    state = response['Reservations'][0]['Instances'][0]['State']['Name']
    if state == 'running':
        print(f"Instance {instance_id} is already running.")
        return
    
    # Start the instance
    ec2_client.start_instances(InstanceIds=[instance_id])
    print(f"Starting instance {instance_id}.")
