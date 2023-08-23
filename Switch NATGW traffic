##########################################################################
# This Python script is intended to operate as an AWS Lambda function.   #
# The main idea is to have N amount of NATGW related CloudWatch alerts,  #
# which in case of alarm state will trigger the Lambda function to check #
# and switch NATGW traffic for X NATGWs in Y AZs received as ENV vars.   #
#                                                                        #
# It could be enhanced with SNS topic notifications                      #
##########################################################################

import json
import os
import boto3

# Checks alert status for a given list of alerts and returns a single OK or ALARM status
def check_az_alarms(alarms_list, client):
    response = client.describe_alarms(
      AlarmNames=alarms_list
    )

    for az_alarm_state in response['MetricAlarms']:
        alarm_name = az_alarm_state['AlarmName']
        alarm_state = az_alarm_state['StateValue']

        if alarm_state != 'OK':
            print(f'Alarm: {alarm_name}, Status: {alarm_state}')
            break
    return alarm_state

# Switches a given route on a given RouteTable. DryRun=True for a test run.
def switch_default_route(rtb_ids, natgw_id, client):
    for rtb_id in rtb_ids:
        print(f'Switching default route towards NAT GW {natgw_id} for RTB ID: {rtb_id}...')
        response = client.replace_route(
            RouteTableId=rtb_id,
            NatGatewayId=natgw_id,
            DestinationCidrBlock='x.x.x.x/x',
            DryRun=False
        )

# The main function which checks the received alarm's AZ and the opposite's alarms' status to decide what further functions to invoke
def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    cloudwatch = boto3.client('cloudwatch')

    alarm_name = event['detail']['alarmName']
    alarm_state = event['detail']['state']['value']

    print(f'Received an event related to ALARM: {alarm_name} with STATE: {alarm_state}. Checking NATGW routing ...')

    az_routing = {
      "az_a": {
        "nat-1": {
          "id": os.environ["NATGW_A"],
          "rtb_ids": [os.environ["ROUTE_TABLE_A"]],
          "alarms": [os.environ["TOTAL_TRAFIC_ALARM_A_NAME"], os.environ["INGRESS_PACKETS_ALARM_A_NAME"]]
        },
        "nat-2": {
          "id": os.environ["NATGW_A2"],
          "rtb_ids": [os.environ["ROUTE_TABLE_A2"]],
          "alarms": [os.environ["TOTAL_TRAFIC_ALARM_A2_NAME"], os.environ["INGRESS_PACKETS_ALARM_A2_NAME"]]
        }
      },
      "az_b": {
        "nat-1": {
          "id": os.environ["NATGW_B"],
          "rtb_ids": [os.environ["ROUTE_TABLE_B"]],
          "alarms": [os.environ["TOTAL_TRAFIC_ALARM_B_NAME"], os.environ["INGRESS_PACKETS_ALARM_B_NAME"]]
        },
        "nat-2": {
          "id": os.environ["NATGW_B2"],
          "rtb_ids": [os.environ["ROUTE_TABLE_B2"]],
          "alarms": [os.environ["TOTAL_TRAFIC_ALARM_B2_NAME"], os.environ["INGRESS_PACKETS_ALARM_B2_NAME"]]
        }
      }
    }

    # Checks an event alarm AZ and the opposite AZ alarms status for the relevant NATGW
    for natgw in az_routing["az_a"]:
        if alarm_name in az_routing["az_a"][natgw]["alarms"]:
            event_alert_az = 'a'
            opposite_az_alarm_state = check_az_alarms(az_routing["az_b"][natgw]["alarms"], cloudwatch)
        elif alarm_name in az_routing["az_b"][natgw]["alarms"]:
            event_alert_az = 'b'
            opposite_az_alarm_state = check_az_alarms(az_routing["az_a"][natgw]["alarms"], cloudwatch)
        else:
            event_alert_az = ''
            print(f'Event alert {alarm_name} is not related to NATGW: {natgw} alarms. Skipping...')

        if event_alert_az == '':
            continue

        if alarm_state == 'OK' and opposite_az_alarm_state == 'OK':
            print(f'Bringing NATGW {natgw} default routes to their default AZs ...')
            for az in az_routing:
                switch_default_route(az_routing[az][natgw]["rtb_ids"], az_routing[az][natgw]["id"], ec2)
        elif alarm_state != 'OK' and opposite_az_alarm_state == 'OK':
            print(f'Putting AZ {event_alert_az.upper()} RTBs with a default route via the opposite AZ NATGW...')
            if event_alert_az == 'a':
                switch_default_route(az_routing["az_a"][natgw]["rtb_ids"], az_routing["az_b"][natgw]["id"], ec2)
            else:
                switch_default_route(az_routing["az_b"][natgw]["rtb_ids"], az_routing["az_a"][natgw]["id"], ec2)
        elif alarm_state == 'OK' and opposite_az_alarm_state != 'OK':
            if event_alert_az == 'a':
                print(f'Switching default routes towards NATGW with id: {az_routing["az_a"][natgw]["id"]} in AZ A...')
                for az in az_routing:
                    switch_default_route(az_routing[az][natgw]["rtb_ids"], az_routing["az_a"][natgw]["id"], ec2)
            else:
                print(f'Switching default routes towards NATGW with id: {az_routing["az_b"][natgw]["id"]} in AZ B...')
                for az in az_routing:
                    switch_default_route(az_routing[az][natgw]["rtb_ids"], az_routing["az_b"][natgw]["id"], ec2)
        elif alarm_state != 'OK' and opposite_az_alarm_state != 'OK':
            print(f'NATGWs with label {natgw} in AZ A and B are DOWN !!!')
        else:
            print('ERROR: Something went wrong while evaluating NATGWs state !')
