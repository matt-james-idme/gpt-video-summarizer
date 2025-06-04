#!/usr/bin/env python3
"""
YouTube Video Summarizer
- Fetches transcript and title of a YouTube video.
- Summarizes the content using a GPT model.
- Improved error handling and clean transcript formatting.
"""

import sys
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from pytube import YouTube
from gpt import complete_chat  # Assumes a project-local wrapper for OpenAI API

def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([entry['text'] for entry in transcript])
    except TranscriptsDisabled:
        print("ERROR: Transcripts are disabled for this video.")
    except NoTranscriptFound:
        print("ERROR: No transcript available for this video.")
    except Exception as e:
        print(f"ERROR: Unexpected exception occurred: {e}")
    return None

def get_video_title(video_id):
    try:
        yt = YouTube(f"https://youtube.com/watch?v={video_id}")
        return yt.title
    except Exception as e:
        print(f"ERROR: Failed to retrieve video title: {e}")
        return "Untitled"

def summarize(transcript, title):
    prompt = (
        f"You are a helpful assistant. Summarize the following YouTube video transcript "
        f"based on its content. The video is titled '{title}'.\n\nTranscript:\n{transcript}"
    )
    return complete_chat(prompt)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python transcribe.py <YouTubeVideoID>")
        sys.exit(1)

    video_id = sys.argv[1]
    transcript = get_transcript(video_id)

    if not transcript:
        print("ERROR: Failed to generate summary.")
        sys.exit(1)

    title = get_video_title(video_id)
    print(f"Video Title: {title}")

    summary = summarize(transcript, title)
    print("\n--- Summary ---\n")
    print(summary)
