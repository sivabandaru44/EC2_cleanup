import boto3
import os
from datetime import datetime, timezone, timedelta
from collections import defaultdict

DAYS_THRESHOLD = 30

def get_ec2_client():
    return boto3.client(
        'ec2',
        region_name=os.getenv('AWS_REGION'),
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )

def is_older_than_threshold(launch_time):
    now = datetime.now(timezone.utc)
    return (now - launch_time) > timedelta(days=DAYS_THRESHOLD)

def process_instances(ec2):
    response = ec2.describe_instances()

    state_count = defaultdict(int)
    instances_to_delete = []
    total_instances = 0

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            total_instances += 1

            instance_id = instance['InstanceId']
            state = instance['State']['Name']
            launch_time = instance['LaunchTime']

            # Count states
            state_count[state] += 1

            # Deletion condition
            if state != 'running' and is_older_than_threshold(launch_time):
                print(f"Eligible for deletion: {instance_id} | State: {state} | Launch: {launch_time}")
                instances_to_delete.append(instance_id)

    return total_instances, state_count, instances_to_delete

def print_summary(total, state_count):
    print("\n========== EC2 SUMMARY ==========")
    print(f"Total Instances: {total}")

    for state, count in state_count.items():
        print(f"{state.upper()} : {count}")

    print("================================\n")

def terminate_instances(ec2, instance_ids):
    if not instance_ids:
        print("No instances to delete.")
        return

    print(f"Terminating instances: {instance_ids}")
    ec2.terminate_instances(InstanceIds=instance_ids)

def main():
    ec2 = get_ec2_client()

    total, state_count, instances = process_instances(ec2)

    print_summary(total, state_count)

    terminate_instances(ec2, instances)

if __name__ == "__main__":
    main()
