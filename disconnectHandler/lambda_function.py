import os
import boto3

CONNECTION_TABLE = os.environ.get("TABLE_NAME")

dynamodb_resource = boto3.resource("dynamodb")
connection_table = dynamodb_resource.Table(CONNECTION_TABLE)


def lambda_handler(event, context):
    connection_table.delete_item(
        Key={
            "connectionId": event["requestContext"]["connectionId"],
        }
    )
    return {"statusCode": 200}
