import json
import boto3
import os

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["STORAGE_USERTABLE_NAME"])

def handler(event, context):
    print("Received event:")
    print(event)

    params = event.get("queryStringParameters", {}) or {}
    user_id = params.get("user_id")
    email = params.get("email")

    if not user_id and not email:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing user_id or email"})
        }

    try:
        if user_id:
            response = table.get_item(Key={"user_id": user_id})
            item = response.get("Item")

            if not item:
                return {
                    "statusCode": 404,
                    "body": json.dumps({"error": "User not found"})
                }

            return success_response(item)

        if email:
            response = table.query(
                IndexName="email-index",
                KeyConditionExpression=boto3.dynamodb.conditions.Key("email").eq(email)
            )
            items = response.get("Items", [])

            if not items:
                return {
                    "statusCode": 404,
                    "body": json.dumps({"error": "User not found"})
                }

            return success_response(items[0])

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

def success_response(data):
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": '*',
            "Access-Control-Allow-Origin": '*',
            "Access-Control-Allow-Methods": 'OPTIONS,POST,GET'
        },
        "body": json.dumps(data)
    }
