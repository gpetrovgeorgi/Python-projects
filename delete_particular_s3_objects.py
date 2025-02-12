###############################################################################
# Finds and deletes S3 objects in a given set of S3 bucket names based        #
# on two regex criterions defined in re_delete and re_other_prefix_delete     # 
# vars.                                                                       #
#                                                                             #
# It could be used either locally or as a deployed AWS Lambda Function with   #
# the relevant IAM role policy permissions and an EventBridge rule to trigger #
# the function on a certain time.                                             #
###############################################################################

import boto3, re

security_buckets = [
    's3_bucket1',
    's3_bucket2'
    's3_bucket3',
]

aws_session = boto3.Session(profile_name="some_aws_profile")
s3 = aws_session.resource('s3')

for s3_bucket in s3_buckets:

    bucket = s3.Bucket(s3_bucket)

    for obj in bucket.object_versions.all():
       re_delete = re.findall('^something', obj.key)
       re_other_prefix_delete = re.findall('^not_bad', obj.key)

       if re_delete or re_other_prefix_delete:
          print("This object: {} from source bucket: {} will be deleted in a second...".format(obj.key, s3_bucket))
          response = bucket.delete_objects(
            Delete={
                'Objects': [
                    {
                        'Key': obj.key,
                        'VersionId': obj.id
                    }
                ]
            }
          )
          print(response)
       else:
          print("Skipping object: {} from source bucket: {}".format(obj.key,s3_bucket))
