#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 09:25:34 2024

@author: robynrosenblum
"""

import subprocess
import whisper
import logging
import os

# # Configure logging
# logging.basicConfig(level=logging.INFO)

def download_and_transcribe_video(url, output_path, nickname):
    # Construct filenames using the nickname
    video_filename = f"{nickname}.webm"
    transcription_file = f"{output_path}/transcript_{nickname}.txt"

    # Download the video
    command = f"yt-dlp -o '{output_path}/{video_filename}' {url}"
    print(f"Executing command: {command}")  # Debug statement
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error downloading video: {result.stderr}")  # Debug statement
        return

    # Construct the full path to the video file
    video_file = f"{output_path}/{video_filename}"
    print(f"Full path to video file: {video_file}")  # Debug statement

    # Check if the video file exists
    if not os.path.exists(video_file):
        print(f"Video file does not exist: {video_file}")  # Debug statement
        return

    # Load the Whisper model
    try:
        model = whisper.load_model("base")
        print("Whisper model loaded successfully.")  # Debug statement
    except Exception as e:
        print(f"Error loading Whisper model: {e}")  # Debug statement
        return

    # Enable verbose logging for Whisper
    print("Starting transcription...")  # Debug statement

    try:
        result = model.transcribe(video_file, verbose=True)
        print("Transcription completed successfully.")  # Debug statement
    except Exception as e:
        print(f"Error during transcription: {e}")  # Debug statement
        return

    # Save transcription to a file
    print(f"Saving transcription to: {transcription_file}")  # Debug statement
    with open(transcription_file, "w") as f:
        f.write(result['text'])

    # Format the transcription (example: remove extra spaces)
    formatted_transcription = result['text'].replace('\n\n', '\n').strip()
    with open(transcription_file, "w") as f:
        f.write(formatted_transcription)

    print("Transcription complete.")  # Debug statement

# Example usage
download_and_transcribe_video("https://www.youtube.com/watch?v=i0SVs_kNlVE", "/Users/robynrosenblum/Downloads", "saylorvideo1")
