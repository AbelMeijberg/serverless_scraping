import boto3


stepfunctions_client = boto3.client('stepfunctions')


def lambda_handler(event, context):
    print(f"State machine starter started with event {event} and context {context}.")

    stepfunctions_client.start_execution(
        stateMachineArn=event['StateMachineArn'],
    )
