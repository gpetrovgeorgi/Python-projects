####################################################################
# This script is intended to be deployed as an AWS Lambda Function #
# which pass through certain S3 object paths and name formats (the #
# time_format var.) in order to confirm there are any log files    #
# uploaded for the current day.                                    #
#                                                                  #
# Please note that the relevant IAM role and policy of the Lambda  #
# function should be also set in place. The same goes for the S3   #
# bucket policy.                                                   #
####################################################################

import boto3
import logging
from datetime import datetime

# Input data for log files scraping
bucket_scan_info = {
  "bucket_a": {
    "log_folders": {
      "system1": {
        "prefix": 'my/prefix/one',
        "time_format": '/%my/%time/%format_a'
      },
      "system2": {
        "prefix": 'my/prefix/two',
        "time_format": '/%my/%time/%format_b'
      },
      "system3": {
        "prefix": 'my/prefix/three',
        "time_format": '/%my/%time/%format_c'
      },
      "system4": {
        "prefix": 'my/prefix/four',
        "time_format": '/%my/%time/%format_d'
      }
    }
  },
  "bucket_b": {
    "log_folders": {
      "system1": {
        "prefix": 'my/other/prefix/one',
        "time_format": '/%my/%other/%time/%format_a'
      }
    }
  }

}

# Returns current date by a given input format
def date_time(s3_log_format):
    current_datetime = datetime.now()
    current_day = current_datetime.strftime(s3_log_format)
    return current_day

# Searches log files in a given particular prefix
# The prefix contains the current day in a specific format provided above
# We need to only be sure that for the current day there is only one log file uploaded for those S3 prefixes
def logs_check(
        bucket_name,
        prefix_path,
        log_format,
        log_system,
        logger
     ):

    s3_client = boto3.client('s3')
    paginator = s3_client.get_paginator('list_objects')
    operation_parameters = {'Bucket': bucket_name,
                            'Prefix': prefix_path}
    page_iterator = paginator.paginate(**operation_parameters)
    s3_log_format = date_time(log_format)

    objects = page_iterator.search(f"Contents[?contains(Key, `{prefix_path}{s3_log_format}`)][]")
    total_log_files = len(list(objects))

    if total_log_files > 0:
        logger.info(f'There are {total_log_files} log files from TODAY in bucket {bucket_name} by {log_system}, with prefix path {prefix_path} and log format {s3_log_format}')
    else:
        logger.info(f'Did not find any log files for TODAY by {log_system} in {bucket_name} with prefix path {prefix_path}, and log format {log_format}')

# Main function, invokes other functions.
def lambda_handler(event, context):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    for bucket in bucket_scan_info:
      for scan_object in bucket_scan_info[bucket]["log_folders"]:
          try:
            logs_check(
                bucket,
                bucket_scan_info[bucket]["log_folders"][scan_object]["prefix"],
                bucket_scan_info[bucket]["log_folders"][scan_object]["time_format"],
                scan_object,
                logger
            )
          except Exception as e:
            logger.error(f'Exception while searching for logs by {scan_object} in {bucket} with prefix path {bucket_scan_info[bucket]["log_folders"][scan_object]["prefix"]}, and time format {bucket_scan_info[bucket]["log_folders"][scan_object]["time_format"]}: {str(e)}')
