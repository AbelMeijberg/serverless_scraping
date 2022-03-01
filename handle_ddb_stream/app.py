from typing import Optional

from boto3.dynamodb.types import TypeDeserializer
from pydantic import BaseModel

deserializer = TypeDeserializer()


class FormattedSocialMediaData(BaseModel):
    id: str
    key1: str
    key2: str
    key3: Optional[str]
    key4: Optional[str]


def dynamo_obj_to_python_obj(dynamo_obj: dict) -> dict:
    """
    Takes a dynamodb low level item (ie. from DDB stream) and parses it to 'normal' json/dict
    """
    return {k: deserializer.deserialize(v) for k, v in dynamo_obj.items()}


def parse_low_level_event(event):
    raw_records = [
        dynamo_obj_to_python_obj(item["dynamodb"]["NewImage"])
        for item in event["Records"]
        if item["eventName"] == "INSERT"
    ]
    return raw_records


def lambda_handler(event, context):
    """
    The event contains the batched records from the DDB stream
    """
    raw_records = parse_low_level_event(event)

    for record in raw_records:
        formatted_record = FormattedSocialMediaData(**record)
        print(formatted_record.dict())
        # Here you would save the formatted record to a database/endpoint of your choice


