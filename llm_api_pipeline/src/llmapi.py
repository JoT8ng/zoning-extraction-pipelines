import json
import boto3
from botocore.exceptions import ClientError

# Using Amazon Bedrock in Canada Central region

class LLMAPI:
    def __init__(self):
        # Assuming that AWS CLI has been configured with credentials and region
        self.bedrock_runtime = boto3.client("bedrock-runtime")

    def query_llm(self, message):
        MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"

        request_body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            # Optional adjust temperature. 0.2 selected for more factual response
            # Indicate response size via max_tokens
            "max_tokens": 50000,
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ]
        })

        try:
            response = self.bedrock_runtime.invoke_model(
                modelId = MODEL_ID,
                body = request_body
            )
            print(response)
            # Read and store raw json response into memory
            response_body = json.loads(response["body"].read())
            print(response_body)
            # Return the response body as a python dictionary
            return response_body["content"][0]["text"]
        # Error handling
        except ClientError as error:
            error_code = error.response['Error']['Code']
            error_message = error.response['Error']['Message']
            raise Exception(f"ClientError: {error_code}, {error_message}")
        except Exception as error:
            raise Exception(f"Error: {str(error)}")