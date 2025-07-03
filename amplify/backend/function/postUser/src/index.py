import json
import boto3
import uuid
import os

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["STORAGE_USERTABLE_NAME"])

def handler(event, context):
    print('Received event:')
    print(event)

    try:
        body = json.loads(event.get("body", "{}"))
        email = body.get("email")

        if not email:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'email' in request"})
            }

        user_id = str(uuid.uuid4())
        table.put_item(Item={"user_id": user_id, "email": email})

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Headers": '*',
                "Access-Control-Allow-Origin": '*',
                "Access-Control-Allow-Methods": 'OPTIONS,POST,GET'
            },
            "body": json.dumps({
                "message": "User created successfully",
                "user_id": user_id
            })
        }

    except Exception as e:
        print(f"Error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
