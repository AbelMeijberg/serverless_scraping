import os
import boto3
from resources.social_media_wrapper import SocialMediaWrapper

API_KEY = os.environ["API_KEY"]
DDB_TABLE = os.environ["DDB_TABLE"]
# initialize the connections outside the handler, lambda best practice
wrapper = SocialMediaWrapper(API_KEY)
ddb_client = boto3.resource("dynamodb")


def lambda_handler(event, context):
    # This would be replaced by your actual api call
    response = wrapper.get_dummy_response()
    table = ddb_client.Table(DDB_TABLE)
    table.put_item(Item=response)
