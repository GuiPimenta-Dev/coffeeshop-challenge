import json
import time
import random


def lambda_handler(event, context):
    query_params = event.get("queryStringParameters", {})
    value = query_params.get("value").lower() if query_params.get("value") else None

    time.sleep(1)
    
    # 30% chance of server error
    if random.random() < 0.3:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "success": False,
                "error": "Could not proccess the payment"
            })
        }

    # Success response
    return {
        "statusCode": 200,
        "body": json.dumps({
            "success": True,
            "message": f"The payment of {value} was processed successfully",
        })
    }