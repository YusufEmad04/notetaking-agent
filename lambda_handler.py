from main import ask

import json


def lambda_handler(event, context):
    body = json.loads(event["body"])
    query = body["query"]

    try:
        response = ask(query)
    except Exception as e:
        # return an error with status code suitable for the error
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
        }

    return {
        "statusCode": 200,
        "body": {"response": response},
        # add all CORS headers
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "*",
        },
    }