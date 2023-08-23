########################################################
# Script which lists EC2 instance realged info such as #
# available regions, EC2 tags, Instance id and type in #
# a given AWS region, in this case eu-central-1.       #      
########################################################

import boto3

client = boto3.client('ec2', region_name='eu-central-1')

response = client.describe_instances()

for ec2 in response["Reservations"]:
    print(
        "This is EC2 with Name Tag: {} ; ID: {} ; Instance Type: {} ; AZ: {}".format(
            ec2["Instances"][0]["Tags"][0]["Value"],
            ec2["Instances"][0]["InstanceId"],
            ec2["Instances"][0]["InstanceType"],
            ec2["Instances"][0]["Placement"]["AvailabilityZone"]
        )
    )

regions = client.describe_regions()

print("\n\n << Those are the available regions: >>\n\n")

for region in regions["Regions"]:
    print(
        "Regions Name: {} ; Endpoint Name: {}".format(
            region["RegionName"], region["Endpoint"]
        )
    )
