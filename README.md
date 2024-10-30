# SummarizeMe: Your Meeting TL;DR App

![SummarizeMe Logo](img/summarize-me.png)

SummarizeMe is an AI-powered app for transcribing meeting recordings, generating summarized meeting notes, extracting key points and action items, and creating video summaries.

This project utilizes Amazon Transcribe for speech-to-text conversion, Amazon Bedrock to summarize meeting transcriptions, and HeyGen for video creation.

Read the full post on [community.aws](https://community.aws/content/2lrAIhZLr6KVb4rGMKqCEarqXbX/summarizeme-your-meeting-tl-dr-app)

## 🎯 Features

- Transcribe audio/video content using Amazon Transcribe
- Summarize meeting transcriptions using Anthropic's Claude 3 Haiku in Amazon Bedrock
- Extract key points and action items from the meeting
- Create video summaries using HeyGen
- Store and search video content using Weaviate vector store
  - Index videos with their metadata
  - Search for related videos using semantic queries

## 🛠 Setup

1. Clone this repository
2. Install required packages: `pip install -r requirements.txt`
3. Configure your AWS and HeyGen credentials in a local `.env` file (see `.env.template` for reference)
4. Ensure you have the necessary permissions set up in your AWS account for:
   - Amazon Transcribe
   - Amazon S3 (for storing temporary audio/video files)
   - Amazon Bedrock (including access to Anthropic Claude 3 Haiku)
5. Start Weaviate Vector Store:
   ```bash
   docker compose -f vector_store/weaviate-docker-compose.yaml up -d
   ```

## 📚 File Structure

- `app.py`: Main application script
- `bedrock/claude_model.py`: Handles interaction with Amazon Bedrock for summarization
- `transcription/transcribe.py`: Manages meeting recording transcription using Amazon Transcribe
- `utils/file_utils.py`: Contains utility functions for file operations
- `video/create_heygen_video.py`: Handles video creation using HeyGen
- `vector_store/`: Contains vector store related files
  - `vector_store_index.py`: Functions for storing and retrieving videos using Weaviate
  - `weaviate-docker-compose.yaml`: Docker configuration for Weaviate
- `.env`: Contains environment variables (not tracked in git)
- `requirements.txt`: Lists Python dependencies

## 🔍 NEW: Weaviate Vector Store & ImageBind

The project now includes a vector store implementation using Weaviate that runs locally via Docker containers. 

This provides a self-hosted vector database that runs entirely on your local machine to store videos and search for related videos using semantic queries. The vector store uses Weaviate's multi2vec-bind module for handling both text and media content, enabling powerful multimodal search capabilities.

To start the vector store:
```bash
docker compose -f vector_store/weaviate-docker-compose.yaml up -d
```

This will start both the Weaviate database and the multi2vec-bind service locally on your machine.

## 🚀 Usage

Make sure the vector store is running. Then, run the main script:

```
python app.py
```

The script will:

1. Prompt you for the input file path
2. Transcribe the audio/video using Amazon Transcribe
3. Summarize the transcription and extract key points and action items using Amazon Bedrock
5. Create a video summary using HeyGen
6. Store the video summary in the vector store
7. Search related videos using semantic queries

The output files will be named:
- `[original_file_name]_transcription.txt`
- `[original_file_name]_key_points.txt`
- `[original_file_name]_action_items.txt`
- `[original_file_name]_video_summary.mp4`

Note: The video summary will be created in your HeyGen account, saved locally, and ingested to the vector store.

## 👀 Example

Here's an example of how to use SummarizeMe with the provided sample files:

1. Ensure you have set up the project as described in the Setup section.
2. Run the script: `python app.py`
3. When prompted for the input file path, enter: `example/alpha_project_meeting.mp3`
4. The script will process the audio file and generate the following outputs in the `example` folder:
   - Transcription: `alpha_project_meeting_transcription.txt`
   - Key points: `alpha_project_meeting_key_points.txt`
   - Action items: `alpha_project_meeting_action_items.txt`
   - Video summary:  `alpha_project_meeting_video_summary.mp4`

## 🎥 Generated Example Video

Check out the generated example video: [SummarizeMe in Action](https://www.youtube.com/watch?v=BZe2EL_zNjQ)

This example demonstrates how SummarizeMe can quickly process a meeting recording and provide valuable insights and summaries.

## 📌 Notes

- Ensure that your AWS account has the necessary permissions and quotas for using Amazon Transcribe, Amazon S3, and Amazon Bedrock services.
- Make sure you have access to the chosen foundation model in Amazon Bedrock.
- The summarization quality depends on the chosen foundation model, inference parameters, and prompt and may vary based on the content and length of the meeting transcription.
- Ensure you have a valid HeyGen API key for video creation functionality.

## 📝 License

This library is licensed under the MIT-0 License. See the LICENSE file.