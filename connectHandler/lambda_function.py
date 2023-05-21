import os
import boto3

CONNECTION_TABLE = os.environ.get("TABLE_NAME")

dynamodb_resource = boto3.resource("dynamodb")
connection_table = dynamodb_resource.Table(CONNECTION_TABLE)


def lambda_handler(event, context):
    try:
        # Client can send additional data via Query String Parameters 
        # qs = event.get("queryStringParameters")
        connection_table.put_item(
            Item={
                "connectionId": event["requestContext"]["connectionId"],
            }
        )
        return {"statusCode": 200}
    except Exception as e:
        print(e)
        return {"statusCode": 500}
