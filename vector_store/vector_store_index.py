"""
Vector store operations module for managing video content using Weaviate.

This module provides functionality to:
- Store videos in a Weaviate vector store
- Search for related videos using text queries
- Handle base64 encoding of media content
"""

import weaviate
import weaviate.classes as wvc
from weaviate.classes.config import Property, DataType
from weaviate.classes.query import MetadataQuery
import base64
import json
import requests
import os
from datetime import datetime, timezone

def json_print(data):
    """
    Print JSON data in a formatted, human-readable way.

    Args:
        data (dict): The JSON data to be pretty-printed
    """
    print(json.dumps(data, indent=2))

def url_to_base64(url):
    """
    Convert an online image URL to base64 encoding.

    Args:
        url (str): The URL of the image to convert

    Returns:
        str: Base64 encoded string of the image

    Raises:
        requests.RequestException: If the image download fails
    """
    image_response = requests.get(url)
    content = image_response.content
    return base64.b64encode(content).decode('utf-8')

def file_to_base64(path):
    """
    Convert a local file to base64 encoding.

    Args:
        path (str): Path to the local file

    Returns:
        str: Base64 encoded string of the file

    Raises:
        IOError: If file reading fails
    """
    with open(path, 'rb') as file:
        return base64.b64encode(file.read()).decode('utf-8')        

def save_video_in_vector_store(video_filename):
# def save_video_in_vector_store(video_filename, transcript):
    """
    Save a video file to the Weaviate vector store with its metadata and transcript.

    Args:
        video_filename (str): Path to the video file to store

    Returns:
        weaviate.Collection: The vector store index object

    Raises:
        weaviate.exceptions.WeaviateException: If vector store operations fail
        IOError: If video file reading fails
    """    
    with weaviate.connect_to_local(port=8080) as client:
        # Delete existing index if it exists
        if (client.collections.exists("index")):
            client.collections.delete("index")

        # Create new collection with schema
        client.collections.create(
            name="index",
            properties=[
                # Property(name="transcript", data_type=DataType.TEXT),
                Property(name="timestamp", data_type=DataType.TEXT),
                Property(name="video", data_type=DataType.BLOB),
                Property(name="name", data_type=DataType.TEXT),
                Property(name="path", data_type=DataType.TEXT),
                Property(name="mediaType", data_type=DataType.TEXT),
            ],            
            vectorizer_config=wvc.config.Configure.Vectorizer.multi2vec_bind(
                text_fields=["timestamp"],
                video_fields=["video"],
            )
        )

        # Get collection reference
        index = client.collections.get("index")

        # Prepare and insert video item
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        item = {
            # "name": os.path.basename(video_filename),
            "name": "video",
            "path": video_filename,
            "video": file_to_base64(video_filename),
            "mediaType": "video",
            "timestamp": timestamp,
            # "transcript": transcript if transcript else ""
        }
        
        # Insert the item
        index.data.insert(item)
        print(f"Inserting video object into the vector store.")

        # Insert some test data 
        item = {
            "name": "video",
            "path": "vector_store/data/cat-clean.mp4",
            "video": file_to_base64("vector_store/data/cat-clean.mp4"),
            "mediaType": "video"
        }
        index.data.insert(item)

        item = {
           "name": "video",
           "path": "vector_store/data/dog-with-stick.mp4",
           "video": file_to_base64("vector_store/data/dog-with-stick.mp4"),
            "mediaType": "video"
        }
        index.data.insert(item)
        print(f"Inserting additional video objects into the vector store for testing.")

        # Validate insertion with aggregation queries
        index = client.collections.get("index")
        index.aggregate.over_all() 

        agg = index.aggregate.over_all(
            group_by="mediaType"
        )

        # Print aggregation results
        for group in agg.groups:
            print(group)

        # Validate with iterator
        itr = index.iterator(
            return_properties=["name", "mediaType"],
        )

        for item in itr:
            print(item.properties)

        return index

def get_related_videos(index, query):
    """
    Search for related videos in the vector store using semantic search.

    Args:
        index (weaviate.Collection): The vector store index
        query (str): Text query to find related videos

    Returns:
        None: Prints paths of related videos to console

    Raises:
        weaviate.exceptions.WeaviateException: If search operation fails
    """
    with weaviate.connect_to_local(port=8080) as client:
        index = client.collections.get("index")

        # Perform semantic search
        response = index.query.near_text(
            query=query,
            return_properties=['name', 'path', 'mediaType', 'video'], 
            return_metadata=MetadataQuery(distance=True),
            limit=5,
        )

        # Print results with distance and similarity scores
        for obj in response.objects:
            print(f"Path: {obj.properties['path']}, Distance: {obj.metadata.distance:.4f}, Similarity: {1 - obj.metadata.distance:.4f}")