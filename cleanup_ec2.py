import boto3
import os
from datetime import datetime, timezone, timedelta

DAYS_THRESHOLD = 30

def get_ec2_client():
    return boto3.client(
        'ec2',
        region_name=os.getenv('AWS_REGION'),
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )

def is_older_than_30_days(launch_time):
    now = datetime.now(timezone.utc)
    return (now - launch_time) > timedelta(days=DAYS_THRESHOLD)

def get_instances_to_delete(ec2):
    response = ec2.describe_instances()
    instances = []

    for res in response['Reservations']:
        for inst in res['Instances']:
            state = inst['State']['Name']
            instance_id = inst['InstanceId']
            launch_time = inst['LaunchTime']

            if state != 'running' and is_older_than_30_days(launch_time):
                print(f"Deleting: {instance_id} | State: {state}")
                instances.append(instance_id)

    return instances

def delete_instances(ec2, instance_ids):
    if instance_ids:
        ec2.terminate_instances(InstanceIds=instance_ids)
        print("Instances terminated")
    else:
        print("No instances to delete")

def main():
    ec2 = get_ec2_client()
    instances = get_instances_to_delete(ec2)
    delete_instances(ec2, instances)

if __name__ == "__main__":
    main()
