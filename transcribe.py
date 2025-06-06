import os
import tempfile
import logging
import sys

from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from pytube import YouTube
import subprocess
from openai import OpenAI
from gpt import summarize_transcript  # Assuming your summarization logic is in gpt.py

from tqdm import tqdm

# Load .env variables
load_dotenv()

# Validate OpenAI key early
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not found. Please set it in a .env file or as an environment variable.")

# Set up OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Logging config
logging.basicConfig(level=logging.INFO, format='[LOG] %(message)s')
logger = logging.getLogger(__name__)

def fetch_transcript(video_id):
    logger.info("Attempting to fetch YouTube transcript...")
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([t["text"] for t in transcript_list])
        logger.info("Successfully fetched transcript via YouTube API.")
        return transcript_text
    except (TranscriptsDisabled, NoTranscriptFound):
        logger.info("No transcript found via YouTube API.")
        return None

def download_audio(video_id):
    logger.info("Downloading audio via yt-dlp...")
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, 'audio.mp3')
        url = f"https://youtube.com/watch?v={video_id}"
        subprocess.run([
            'yt-dlp',
            '--extract-audio',
            '--audio-format', 'mp3',
            '-o', os.path.join(tmpdir, 'audio.%(ext)s'),
            url
        ], check=True)
        return output_path

def transcribe_audio(path):
    logger.info("Transcribing audio with OpenAI Whisper API (new SDK)...")
    try:
        with open(path, "rb") as audio_file:
            with tqdm(desc="[WAIT] Whisper API processing", bar_format="{desc} {bar}") as pbar:
                transcript_obj = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
                pbar.update(1)
        return transcript_obj.text
    except Exception as e:
        logger.error(f"Whisper transcription failed: {e}")
        return None

def extract_title(video_id):
    try:
        yt = YouTube(f"https://youtube.com/watch?v={video_id}")
        return yt.title
    except Exception:
        return "Untitled"

def main(video_id):
    transcript = fetch_transcript(video_id)
    if not transcript:
        audio_path = download_audio(video_id)
        transcript = transcribe_audio(audio_path)

    if not transcript:
        logger.error("Failed to retrieve transcript by any method.")
        return

    title = extract_title(video_id)
    print("\n--- Structured Summary ---\n")
    print(summarize_transcript(transcript, title))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python transcribe.py <youtube_video_id>")
        sys.exit(1)
    video_id = sys.argv[1]
    main(video_id)
