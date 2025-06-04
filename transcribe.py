#!/usr/bin/env python3
"""
Updated YouTube Video Summarizer
- Uses latest openai.ChatCompletion endpoint for GPT models.
- Enhanced error handling, logging, and modular code.
"""

import os
import logging
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import openai
import argparse

# Load environment variables from .env, if available
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def get_transcript(video_id: str) -> str:
    """
    Retrieve the transcript for a given YouTube video id.
    """
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([entry["text"] for entry in transcript_list])
        logging.info("Transcript retrieved successfully.")
        return transcript
    except TranscriptsDisabled:
        logging.error("Transcripts are disabled for this video.")
        raise
    except NoTranscriptFound:
        logging.error("No transcript found for this video.")
        raise
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise


def generate_summary(transcript: str, max_tokens: int = 150, temperature: float = 0.7) -> str:
    """
    Generate a summary using OpenAI's ChatCompletion API.
    """
    # Prepare the system and user prompts
    system_prompt = "You are a helpful assistant summarizing YouTube video transcripts."
    user_prompt = (
        "Generate a concise summary of the following transcript. "
        "Include a title, an introductory sentence, bullet points for major topics, and a concluding sentence.\n"
        f"Transcript: {transcript}"
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or use gpt-4 if available
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        summary = response["choices"][0]["message"]["content"]
        logging.info("Summary generated successfully.")
        return summary
    except Exception as e:
        logging.error(f"Error in generating summary: {e}")
        raise


def parse_args():
    parser = argparse.ArgumentParser(description="Summarize a YouTube video using GPT")
    parser.add_argument("video_id", help="YouTube video ID (the alphanumeric code in the URL)")
    parser.add_argument("--max_tokens", type=int, default=150, help="Max tokens for the summary")
    parser.add_argument("--temperature", type=float, default=0.7, help="Temperature for GPT API")
    return parser.parse_args()


def main():
    args = parse_args()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        logging.error("OPENAI_API_KEY is not set in the environment.")
        return

    openai.api_key = openai_api_key

    try:
        transcript = get_transcript(args.video_id)
        summary = generate_summary(transcript, max_tokens=args.max_tokens, temperature=args.temperature)
        print("\n--- Video Summary ---\n")
        print(summary)
    except Exception as e:
        logging.error("Failed to generate summary.")


if __name__ == "__main__":
    main()
