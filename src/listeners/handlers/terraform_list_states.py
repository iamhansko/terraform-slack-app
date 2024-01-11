import os
import boto3

TERRAFROM_STATE_S3_BUCKET_NAME = os.getenv('TERRAFROM_STATE_S3_BUCKET_NAME')

def handler(body, respond):
    s3 = boto3.client('s3')
    
    states = s3.list_objects(Bucket=TERRAFROM_STATE_S3_BUCKET_NAME, Delimiter='/')
      
    if not(states.get('CommonPrefixes') is None or len(states.get('CommonPrefixes')) == 0):
        respond(
            blocks=[
                {
                    "type": "divider"
                }
            ]
        )
        for state in states.get('CommonPrefixes'):
            folder = state.get('Prefix')[0:-1]
            respond(
                blocks=[
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"📁 *{folder}*"
                        }
                    }
                ]
            )
        respond(
            blocks=[
                {
                    "type": "divider"
                }
            ]
        )
    else:
        respond(
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"저장된 State가 없습니다. (No Terraform State)"
                    }
                }
            ]
        )
