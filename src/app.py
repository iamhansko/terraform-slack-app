import os
import sys
from slack_bolt import App 
from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_bolt.adapter.aws_lambda import SlackRequestHandler
from slack_bolt.adapter.aws_lambda.lambda_s3_oauth_flow import LambdaS3OAuthFlow
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from listeners import commands

SLACK_CLIENT_ID = os.getenv("SLACK_CLIENT_ID")
SLACK_CLIENT_SECRET = os.getenv("SLACK_CLIENT_SECRET")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")
OAUTH_STATE_S3_BUCKET_NAME = os.getenv("OAUTH_STATE_S3_BUCKET_NAME")
INSTALLATION_S3_BUCKET_NAME = os.getenv("INSTALLATION_S3_BUCKET_NAME")

app = App(
    process_before_response = True,
    signing_secret = SLACK_SIGNING_SECRET,
    oauth_flow = LambdaS3OAuthFlow(
        settings=OAuthSettings(
            client_id = SLACK_CLIENT_ID,
            client_secret = SLACK_CLIENT_SECRET,
            scopes = [
                'commands'
            ],
        ),
        oauth_state_bucket_name = OAUTH_STATE_S3_BUCKET_NAME,
        installation_bucket_name = INSTALLATION_S3_BUCKET_NAME,
    ),
)

commands.listener(app)

def lambda_handler(event, context):
    slack_handler = SlackRequestHandler(app=app)
    return slack_handler.handle(event, context)