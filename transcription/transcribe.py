import boto3
import time
import requests
import os
import uuid

def transcribe_meeting(input_file_path):
    """
    Transcribe the input file using Amazon Transcribe.

    This function performs the following steps:
    1. Uploads the input file to an S3 bucket.
    2. Initiates a transcription job using Amazon Transcribe.
    3. Waits for the job to complete.
    4. Retrieves and returns the transcribed text.

    Args:
        input_file_path (str): Path to the input file.

    Returns:
        str: The transcribed text.

    Raises:
        Exception: If the transcription job fails or if there's an error in file upload.
    """
    transcribe = boto3.client('transcribe')
    job_name = f"TranscribeJob_{os.path.basename(input_file_path).split('.')[0]}_{uuid.uuid4().hex[:8]}"
    
    # Upload the video file to S3
    s3 = boto3.client('s3')
    bucket_name = os.getenv('S3_BUCKET_NAME')
    s3_key = f"video/{os.path.basename(input_file_path)}"
    s3.upload_file(input_file_path, bucket_name, s3_key)
    
    job_uri = f"s3://{bucket_name}/{s3_key}"
    
    # Start the transcription job
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        LanguageCode='en-US'
    )

    print("Transcription job started. Waiting for completion...")
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        time.sleep(10)

    if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        result = requests.get(status['TranscriptionJob']['Transcript']['TranscriptFileUri'])
        return result.json()['results']['transcripts'][0]['transcript']
    else:
        raise Exception(f"Transcription failed: {status['TranscriptionJob']['FailureReason']}")