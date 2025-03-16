import json
import time
import random

ALLOWED_STATUSES = {"waiting", "preparation", "ready", "delivered", "canceled"}

def lambda_handler(event, context):
    query_params = event.get("queryStringParameters", {})
    status = query_params.get("status").lower() if query_params.get("status") else None

    if not status:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": "Missing required query parameter: status"
            })
        }

    if status not in ALLOWED_STATUSES:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": f"Invalid status '{status}'. Allowed values: {', '.join(ALLOWED_STATUSES)}"
            })
        }

    # Simulate server delay between 4-8 seconds
    delay = random.uniform(4, 8)
    time.sleep(delay)
    
    # Success response
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"The email was sent with the status {status}",
        })
    }