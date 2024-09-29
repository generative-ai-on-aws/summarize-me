import boto3
import json
import os

def summarize_meeting(transcription):
    """
    Summarize the meeting transcription using Amazon Bedrock's Claude 3 Haiku model via the Converse API.

    This function performs the following steps:
    1. Initializes the Bedrock client.
    2. Sets up the inference configuration for the Claude 3 Haiku model.
    3. Sends the transcription to the model for summarization.
    4. Processes the model's response to extract key points and action items.

    Args:
        transcription (str): The meeting transcription.

    Returns:
        tuple: A tuple containing two strings: key points and action items.

    Raises:
        Exception: If the summarization fails or if there's an error in communicating with the Bedrock API.
    """
    bedrock = boto3.client('bedrock-runtime', region_name=os.getenv('AWS_REGION', 'us-east-1'))
    
    # model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"
    model_id = "anthropic.claude-3-haiku-20240307-v1:0"
    inference_config = {
        "temperature": 0.5,
        "topP": 0.9,
        "maxTokens": 1000
    }

    def make_api_call(prompt):
        try:
            print(f"Preparing to call Bedrock API with converse()")
            response = bedrock.converse(
                modelId=model_id,
                messages=[{"role": "user", "content": [{"text": prompt}]}],
                inferenceConfig=inference_config
            )
            print("API call completed")

            if 'output' in response and 'message' in response['output']:
                return response['output']['message']['content'][0]['text']
            else:
                print("Unexpected response format")
                return ""
        except Exception as e:
            raise Exception(f"Failed to summarize meeting: {str(e)}")

    key_points_prompt = f"Provide a bullet list of max 5 key points discussed in the following meeting transcription. Don't include any action items. Start directly with the bullet list, don't add any introduction:\n\n{transcription}"
    action_items_prompt = f"Provide a bullet list of max 5 action items from the following meeting transcription. Start directly with the bullet list, don't add any introduction:\n\n{transcription}"

    key_points = make_api_call(key_points_prompt)
    action_items = make_api_call(action_items_prompt)

#    print("Key Points:\n", key_points)
#    print("Action Items:\n", action_items)

    return key_points, action_items