########################################################
# Lists AWS ECR images and finds their retention time. #
########################################################

import boto3
import json
from datetime import datetime, timedelta
from pytz import timezone

def generate_image_tags(envs, instances, types):
    tags = [f'{e}_{i}_{t}' for e in envs for i in instances for t in types if not (e == 'env1' and i == 'ins2')]
    return tags

profiles = [
    "account1",
    "account2",
    "account3"
]
envs = ["env1", "env2", "env3"]
instances = ["ins1", "ins2"]
image_tags_data = {
    "account1": {
         "repo1": generate_image_tags(envs, instances, ["tag1", "tag2"]),
         "repo2": ["tag3"],
         "repo3": generate_image_tags(envs, instances, ["tag1"])
    },
    "account2": {
        "repo1": ["tag1"],
        "repo2": ["tag2"],
        "repo3": ["tag3"]
    },
    "account3": {
        "repo1": ["tag4", "tag5"]
    }
}

for profile in profiles:
    session = boto3.Session(profile_name=profile)
    ecr = session.client('ecr')

    repos = ecr.describe_repositories()["repositories"]
    repo_names = []

    # Collect all repo names
    for r in repos:
        repo_name = r["repositoryName"]

        if 'repo1' in repo_name.lower():
            continue
        if 'some_string' in repo_name.lower() and profile == 'account3':
            continue

        if not 'test_string' in repo_name.lower():
            repo_names.append(repo_name)

    for repo in repo_names:
        image_tags = image_tags_data[profile][repo]

        # Find the lifecycle policy days
        lifecycle_policy = json.loads(ecr.get_lifecycle_policy(repositoryName=repo)["lifecyclePolicyText"])
        retention_days = lifecycle_policy["rules"][0]["selection"]["countNumber"]

        for tag in image_tags:
            try:
                image = ecr.describe_images(
                    repositoryName=repo,
                    imageIds=[{'imageTag': tag}]
                )
                # Get image push date
                image_push_date = image["imageDetails"][0]["imagePushedAt"]

                # Calculate image end date according to what is set as ECR lifecycle policy
                expiration_time = image_push_date + timedelta(days=retention_days)

                # Get image remaining days until expiration
                time_remaining = (expiration_time - datetime.now(timezone('Europe/Sofia'))).days

                if 'account1' in profile.lower():
                  p = 'Account_1'
                elif 'account2' in profile.lower():
                  p = 'Account_2'
                else:
                  p = 'Account_3'
                print(f'{p} {repo} {tag} {time_remaining}d')

            except Exception:
                print(f'{p} {repo} {tag} Not found')
