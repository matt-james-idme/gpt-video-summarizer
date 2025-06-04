#!/usr/bin/env python3
"""
YouTube Video Summarizer with Whisper Fallback and Structured GPT Summary
- Attempts to fetch transcript via YouTube API
- Falls back to Whisper (OpenAI) if needed
- Summarizes using GPT-4 with structured prompt
"""

import os
import sys
import subprocess
import tempfile
import threading
import time
import openai
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

# Set API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")

def log(msg):
    print(f"[LOG] {msg}")

def get_transcript(video_id):
    try:
        log("Attempting to fetch YouTube transcript...")
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([entry['text'] for entry in transcript])
    except TranscriptsDisabled:
        log("Transcripts are disabled for this video.")
    except NoTranscriptFound:
        log("No transcript found via YouTube API.")
    except Exception as e:
        log(f"Unexpected transcript error: {e}")
    return None

def download_audio(video_id):
    log("Downloading audio via yt-dlp...")
    url = f"https://youtube.com/watch?v={video_id}"
    tmp_dir = tempfile.mkdtemp()
    audio_path = os.path.join(tmp_dir, "audio.mp3")
    command = [
        "yt-dlp",
        "-x", "--audio-format", "mp3",
        "-o", audio_path,
        url
    ]
    try:
        subprocess.run(command, check=True)
        return audio_path
    except subprocess.CalledProcessError as e:
        log(f"Audio download failed: {e}")
        return None

def transcribe_whisper(audio_path):
    log("Transcribing audio with OpenAI Whisper API (new SDK)...")

    spinner_running = True

    def spinner():
        while spinner_running:
            for ch in "|/-\\":
                print(f"\r[WAIT] Whisper API processing... {ch}", end="", flush=True)
                time.sleep(0.2)

    spinner_thread = threading.Thread(target=spinner)
    spinner_thread.start()

    try:
        with open(audio_path, "rb") as f:
            transcript = openai.audio.transcriptions.create(
                model="whisper-1",
                file=f
            )
            return transcript.text
    except Exception as e:
        print()
        log(f"Whisper transcription failed: {e}")
        return None
    finally:
        spinner_running = False
        spinner_thread.join()
        print("\r[LOG] Whisper transcription complete.        ")

def get_video_title(video_id):
    try:
        yt = YouTube(f"https://youtube.com/watch?v={video_id}")
        return yt.title
    except Exception as e:
        log(f"Failed to fetch video title: {e}")
        return "Untitled"

def summarize(transcript, title):
    log("Summarizing with GPT...")
    prompt = (
        f"You are a helpful assistant. Analyze the following YouTube transcript titled '{title}' and provide:\n"
        f"- A concise summary of the main ideas\n"
        f"- A list of key points or arguments\n"
        f"- Any actionable steps or instructions mentioned\n"
        f"- Any statistics, data points, or factual claims\n\n"
        f"Transcript:\n{transcript}"
    )
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes YouTube videos."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=1000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        log(f"GPT summarization failed: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python transcribe.py <YouTubeVideoID>")
        sys.exit(1)

    video_id = sys.argv[1]
    transcript = get_transcript(video_id)

    if not transcript:
        audio_path = download_audio(video_id)
        if audio_path:
            transcript = transcribe_whisper(audio_path)

    if not transcript:
        log("Failed to retrieve transcript by any method.")
        sys.exit(1)

    title = get_video_title(video_id)
    log(f"Video Title: {title}")

    summary = summarize(transcript, title)
    if summary:
        print("\n--- Structured Summary ---\n")
        print(summary)
    else:
        log("Failed to generate summary.")
