import os
import json
import boto3

CONNECTION_TABLE = os.environ.get("TABLE_NAME")

dynamodb_resource = boto3.resource("dynamodb")
connection_table = dynamodb_resource.Table(CONNECTION_TABLE)

def lambda_handler(event, context):
    connections = []
    try:
        connection_response = connection_table.scan()
        connections = connection_response["Items"]
    except Exception as e:
        print(e)
        return {"statusCode": 500}
    
    current_connection_id = event["requestContext"]["connectionId"]
    domain = event["requestContext"]["domainName"]
    client = boto3.client(
        "apigatewaymanagementapi",
        endpoint_url=f'https://{domain}/{event["requestContext"]["stage"]}',
    )
    
    body = json.loads(event["body"])
    message = body["message"]
    is_failed = False

    # Broadcasts message to all users except self
    for connection in connections:

        if current_connection_id == connection["connectionId"]:
            continue

        try:
            client.post_to_connection(
                Data=bytes(message, 'utf-8'),
                ConnectionId=connection["connectionId"],
            )
        except Exception as e:
            is_failed = True
            print(e)

    if is_failed:
        return {"statusCode": 500}
    
    return {"statusCode": 200}