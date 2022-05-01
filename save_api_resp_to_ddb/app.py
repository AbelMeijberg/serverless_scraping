import os
import boto3
from resources.social_media_wrapper import SocialMediaWrapper


API_KEY = os.environ["API_KEY"]
DDB_TABLE = os.environ["DDB_TABLE"]
QUEUE_TABLE = os.environ["QUEUE_TABLE"]

# initialize the connections outside the handler, lambda best practice
wrapper = SocialMediaWrapper(API_KEY)
ddb_client = boto3.resource("dynamodb")


def get_request_id() -> str:
    table = ddb_client.Table(QUEUE_TABLE)
    response = table.scan(Limit=1)
    try:
        return response["Items"][0]["id"]
    except IndexError:
        return None


def delete_request_id(request_id: str):
    table = ddb_client.Table(QUEUE_TABLE)
    table.delete_item(Key={"id": request_id})


def lambda_handler(event, context):
    print(event)
    # We initialize the variables that we pass to the state machine
    sm_execution_count = event["input"]["execution_count"] + 1
    sm_done = False
    sm_wait_until = None

    # We read an item from the Queue table, if it returns None we are done
    request_id = get_request_id()
    
    if request_id is None:
        sm_done = True
    else:
        # This would be replaced by your actual api call
        response = wrapper.get_dummy_response(request_id)

        table = ddb_client.Table(DDB_TABLE)
        table.put_item(Item=response)

        print(request_id, type(request_id))
        delete_request_id(request_id)

        # Check if the rate limit is hit and if we are done
        if wrapper.check_if_rate_limit_hit():
            sm_wait_until = wrapper.get_ratelimit_reset_time()

    lambda_output = {
        "execution_count": sm_execution_count,
        "wait_until": sm_wait_until,
        "done": sm_done,
    }

    return lambda_output
