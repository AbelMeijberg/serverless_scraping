import os
import boto3
from resources.social_media_wrapper import SocialMediaWrapper


API_KEY = os.environ['API_KEY']
DDB_TABLE = os.environ['DDB_TABLE']

# initialize the connections outside the handler, lambda best practice
wrapper = SocialMediaWrapper(API_KEY)
ddb_client = boto3.resource('dynamodb')


def lambda_handler(event, context):
    print(event)
    # We initialize the variables that we pass to the state machine
    sm_execution_count = event["input"]["execution_count"] + 1
    sm_done = False
    sm_wait_until = None

    # Here we would get some input information (ie request id) about the request to make,
    # from the input event or a DDB table

    # This would be replaced by your actual api call
    response = wrapper.get_dummy_response()

    table = ddb_client.Table(DDB_TABLE)
    table.put_item(Item=response)

    # Check if the rate limit is hit and if we are done
    if wrapper.check_if_rate_limit_hit():
        sm_wait_until = wrapper.get_ratelimit_reset_time()

    # Here we would check if we are done with making api calls, for example if our DDB queue tabel is empty

    lambda_output = {
        "execution_count": sm_execution_count,
        "wait_until": sm_wait_until,
        "done": sm_done
    }

    return lambda_output


