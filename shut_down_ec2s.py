#####################################################################
# Accepts a list of AWS regions to check in via regions var.        #
# Then passes through each of the regions and checks the EC2        #
# instances state and tags. If it does not find some custom tag     #
# shuts down each one of the instances if the same is in running    #
# state.                                                            #
#                                                                   #
# The main idea for this script is to be deployed as an AWS Lambda  #
# function with relevant IAM role policy. It will be triggered by   #
# an EventBridge rule once per day. The EventBridge rule should     #
# also have the permission to trigger the Lambda function.          #
#                                                                   #
# The function could be also enhanced with SNS topic notifications. #
#####################################################################

import boto3

regions = [
    'eu-west-2',
    'eu-west-3',
    'eu-south-1'
]

# Stops a given EC2 by its id
def stop_instance(client, instance_id):
    response = client.stop_instances(
        InstanceIds=[
            instance_id,
        ],
        DryRun=False,
        Force=True
    )
    previous_state = response["StoppingInstances"][0]["PreviousState"]["Name"]
    current_state = response["StoppingInstances"][0]["CurrentState"]["Name"]

    print(f'''
        Stopping instance: {instance_id}, please wait ...
        Previous state: {previous_state},
        Current state: {current_state}
    ''')

# Checks the instances tags and state
def main(region):
    aws_session = boto3.Session(
      profile_name="some_profile_name", 
      region_name=some_region_name
    )
    client = aws_session.client('ec2')
    response = client.describe_instances()
    custom_tag = 'no'

    if response["Reservations"]:
        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                instance_state = instance["State"]["Name"]
                instance_id = instance["InstanceId"]
                instance_az = instance["Placement"]["AvailabilityZone"]
                instance_tags = instance["Tags"]

                if instance_state != 'running':
                    print(f'Instance: {instance_id} is in {instance_state} state. Nothing to do here ...')
                    continue
                else:
                    print(f'Scanning Instance with ID: {instance_id}, AZ: {instance_az}, State: {instance_state}')
                    if instance_tags:
                        for tag in instance_tags:
                            if tag["Key"].lower() == 'custom tag name' and tag["Value"].lower() == 'yes':
                                print(f'Instance: {instance_id} is created with a < custom tag name > tag. Skipping ...')
                                custom_tag = 'yes'
                                continue

                    if custom_tag == 'no':
                        print(f'Shutting down Instance with ID: {instance_id}...')
                        stop_instance(client, instance_id)

                print('---------------------------------------------')
    else:
        print(f'DID NOT FIND EC2 INSTANCES in REGION: {region}')
    print(f'REGION: {region} SCAN FINISHED\n')

for region in regions:
    main(region)
