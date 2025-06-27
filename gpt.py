import ssl
import certifi
ssl._create_default_https_context = ssl.create_default_context(cafile=certifi.where())

import os
import tempfile
import logging
import sys
import subprocess
import shutil

from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from pytube import YouTube
from openai import OpenAI
from gpt import summarize_transcript
from tqdm import tqdm

# Load environment variables from .env
load_dotenv()

# Validate API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not found. Please set it in a .env file or as an environment variable.")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Configure logging
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
    except Exception as e:
        logger.error(f"Transcript fetch failed due to unexpected error: {e}")
        return None

def download_audio(video_id):
    logger.info("Downloading audio via yt-dlp...")

    if not shutil.which("yt-dlp"):
        logger.error("'yt-dlp' not found in PATH. Please install it.")
        print("❌ yt-dlp is not installed. Use `brew install yt-dlp` or `pipx install yt-dlp`.")
        return None

    if not shutil.which("ffmpeg"):
        logger.warning("⚠ 'ffmpeg' not found in PATH. Audio conversion may fail.")

    with tempfile.TemporaryDirectory() as tmpdir:
        output_template = os.path.join(tmpdir, 'audio.%(ext)s')
        url = f"https://youtube.com/watch?v={video_id}"
        try:
            subprocess.run([
                'yt-dlp',
                '--extract-audio',
                '--audio-format', 'mp3',
                '--postprocessor-args', 'ffmpeg:-t 600',  # limit to first 10 minutes
                '-o', output_template,
                url
            ], check=True)

            files = os.listdir(tmpdir)
            logger.info(f"Files in temp dir: {files}")

            for ext in (".mp3", ".webm"):
                for file in files:
                    if file.endswith(ext):
                        source = os.path.join(tmpdir, file)
                        stable_temp = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
                        with open(source, "rb") as src, open(stable_temp.name, "wb") as dst:
                            dst.write(src.read())

                        if os.path.getsize(stable_temp.name) > 26_214_400:
                            logger.error("Audio file exceeds Whisper API size limit (25 MB).")
                            print("❌ Audio file too large for Whisper API. Try a shorter video.")
                            return None

                        return stable_temp.name

            raise FileNotFoundError("yt-dlp did not produce an .mp3 or .webm file — is ffmpeg installed?")
        except Exception as e:
            logger.error(f"yt-dlp audio download failed: {e}")
            return None

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
    print(f"[DEBUG] Starting transcription for video ID: {video_id}")

    transcript = fetch_transcript(video_id)
    if not transcript:
        audio_path = download_audio(video_id)
        if not audio_path:
            logger.error("Audio download failed. Cannot proceed with transcription.")
            print("❌ Audio download failed. Exiting.")
            return
        transcript = transcribe_audio(audio_path)

    if not transcript:
        logger.error("Failed to retrieve transcript by any method.")
        print("❌ No transcript was generated. Exiting.")
        return

    title = extract_title(video_id)
    summary = summarize_transcript(transcript, title)

    print("\nChoose output format:")
    print("1. Print to terminal")
    print("2. Save as Markdown (.md)")
    print("3. Save as Plain Text (.txt)")
    choice = input("Enter 1, 2, or 3: ").strip()

    if choice == "1":
        print("\n--- Structured Summary ---\n")
        print(summary)
    elif choice == "2":
        filename = f"{video_id}_summary.md"
        with open(filename, "w") as f:
            f.write(f"# Summary for: {title}\n\n{summary}")
        logger.info(f"Summary saved to {filename}")
    elif choice == "3":
        filename = f"{video_id}_summary.txt"
        with open(filename, "w") as f:
            f.write(f"Summary for: {title}\n\n{summary}")
        logger.info(f"Summary saved to {filename}")
    else:
        print("❌ Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python transcribe.py <youtube_video_id>")
        sys.exit(1)
    video_id = sys.argv[1]
    main(video_id)
