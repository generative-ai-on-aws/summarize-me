import os
import sys
from dotenv import load_dotenv
from transcription.transcribe import transcribe_meeting
from bedrock.claude_model import summarize_meeting
from utils.file_utils import save_to_file
from video.create_heygen_video import create_heygen_video
from video.create_heygen_video import wait_for_heygen_video_completion
from vector_store.vector_store_index import save_video_in_vector_store
from vector_store.vector_store_index import get_related_videos

def main():
    """
    Main function to process a meeting recording and create a summary video.
    
    This function performs the following steps:
    1. Prompts the user for an input file path.
    2. Validates the input file.
    3. Transcribes the meeting using Amazon Transcribe.
    4. Summarizes the transcription using Amazon Bedrock.
    5. Saves the transcription, key points, and action items to separate files.
    6. Creates a summary video using HeyGen API.
    
    Raises:
        FileNotFoundError: If the input file is not found.
        ValueError: If the input file type is not supported.
        Exception: If an error occurs during transcription, summarization, or video creation.
    """
    # Load environment variables from .env
    load_dotenv()
    try:
        # Get input file path and validate
        input_file = input("\n\nEnter the path to the input file: ")
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")
        # Check for supported file types for Amazon Transcribe
        if not any(input_file.lower().endswith(ext) for ext in ['.amr', '.flac', '.m4a', '.mp3', '.mp4', '.ogg', '.wav', '.webm']):     
            raise ValueError("Input file type not supported. Try an .mp3 or .mp4 file.")
                
        # Transcribe video using Amazon Transcribe
        print("\n\n==== (1) Transcribing input file...")
        transcription = transcribe_meeting(input_file)
        if not transcription:
            print("Warning: Transcription is empty.")
            
        # Save transcription to output file
        transcription_file = os.path.splitext(input_file)[0] + "_transcription.txt"
        save_to_file(transcription, transcription_file)
        print(f"Transcription saved to {transcription_file}")
        
        # Summarize transcription using Amazon Bedrock
        print("\n\n==== (2) Summarizing meeting...")
        try:
            key_points, action_items = summarize_meeting(transcription)
            if not key_points and not action_items:
                print("Warning: Generated key points and action items are empty.")
            # Save key points and action items to output files
            key_points_file = os.path.splitext(input_file)[0] + "_key_points.txt"
            action_items_file = os.path.splitext(input_file)[0] + "_action_items.txt"
            save_to_file(key_points, key_points_file)
            save_to_file(action_items, action_items_file)
            print(f"Key points saved to {key_points_file}")
            print(f"Action items saved to {action_items_file}")
        except Exception as e:
            print(f"Error during summarization: {str(e)}")
            raise
        
        # Create video using HeyGen
        print("\n\n==== (3) Creating video...")
        try:
            # Create first part with key points discussed
            meeting_name = os.path.splitext(os.path.basename(input_file))[0]
            title1 = f"{meeting_name} - Key Points"
            bullet_point_list1 = key_points.splitlines()
            speaker_script_paragraph_list1 = f"Here are the key points discussed in the meeting.\n\n{key_points}"[:800]

            # Create second part with action items
            title2 = f"{meeting_name} - Action Items"
            bullet_point_list2 = action_items.splitlines()
            speaker_script_paragraph_list2 = f"Here are the top 5 action items from the meeting:\n{action_items}"[:800]

            # Create video            
            video_id = create_heygen_video(meeting_name, title1, bullet_point_list1, speaker_script_paragraph_list1, title2, bullet_point_list2, speaker_script_paragraph_list2)

            # Wait for video processing to complete and save as a given filename
            video_filename = f"example/{meeting_name}_video_summary.mp4"
            wait_for_heygen_video_completion(video_id, video_filename)
        except Exception as e:
            print(f"Error during video creation: {str(e)}")
            raise

        try:
            # Store video and transcript in vector store 
            print(f"\n\n==== (4) Saving video to vector store: {video_filename}")
            index = save_video_in_vector_store(video_filename)
            # index = save_video_in_vector_store(video_filename, transcription)

            # Get videos for a given query
            # query_string = meeting_name
            query_string = "action items"
            print(f"\n\n==== (5) Retrieving related videos for: {query_string} ...")
            get_related_videos(index, query_string)
            #print(related_video_filenames)
        except Exception as e:
            print(f"Error during video save/retrieve: {str(e)}")
    except FileNotFoundError as e:
        print(f"File error: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Input error: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()