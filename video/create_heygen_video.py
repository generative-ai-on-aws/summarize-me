import requests
import os

def create_heygen_video(meeting_name, title1, bullet_point_list1, speaker_script_paragraph_list1, title2, bullet_point_list2, speaker_script_paragraph_list2):
    """
    Create a video using the Heygen API with the provided meeting information.

    Args:
        meeting_name (str): The name of the meeting.
        title1 (str): The title for the first section of the video.
        bullet_point_list1 (list): A list of bullet points for the first section.
        speaker_script_paragraph_list1 (list): A list of paragraphs for the speaker script of the first section.
        title2 (str): The title for the second section of the video.
        bullet_point_list2 (list): A list of bullet points for the second section.
        speaker_script_paragraph_list2 (list): A list of paragraphs for the speaker script of the second section.

    Returns:
        dict: The response from the Heygen API containing video creation information.

    Raises:
        Exception: If there's an error in creating the video or communicating with the Heygen API.
    """
    print(f"Creating video for {meeting_name}")

    template_id = os.getenv('HEYGEN_TEMPLATE_ID')
    api_key = os.getenv('HEYGEN_API_KEY')
    headers = {"Accept": "application/json", "X-API-KEY": api_key}

    generate_url = f"https://api.heygen.com/v2/template/{template_id}/generate"
    payload = {
        "test": False,
        "caption": False,
        "title": meeting_name,
        "variables": {
            "meeting_name": {
                "name": "meeting_name",
                "type": "text",
                "properties": {"content": meeting_name},
            },
            "title1": {
                "name": "title1",
                "type": "text",
                "properties": {"content": title1},
            },
            "body1": {
                "name": "body1",
                "type": "text",
                "properties": {"content": "\n".join(bullet_point_list1)},
            },
            "script1": {
                "name": "script1",
                "type": "text",
                "properties": {"content": speaker_script_paragraph_list1},
            },
            "title2": {
                "name": "title2",
                "type": "text",
                "properties": {"content": title2},
            },
            "body2": {
                "name": "body2",
                "type": "text",
                "properties": {"content": "\n".join(bullet_point_list2)},
            },
            "script2": {
                "name": "script2",
                "type": "text",
                "properties": {"content": speaker_script_paragraph_list2},
            },
        },
    }
    headers["Content-Type"] = "application/json"
    response = requests.post(generate_url, headers=headers, json=payload)
    if not response.json()["data"]:
        print(response)
        print(response.json()["error"])
        exit()
    video_id = response.json()["data"]["video_id"]
    print(f"video_id: {video_id}")