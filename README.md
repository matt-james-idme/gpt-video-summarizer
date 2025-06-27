# GPT Video Summarizer

A CLI tool that transcribes and summarizes YouTube videos using a fallback-based approach. It first attempts to retrieve the video transcript via the YouTube Transcript API. If that fails, it downloads and transcribes audio using OpenAI's Whisper API, then summarizes the result using GPT (via `gpt.py`).

## Features

- Attempts transcript retrieval via `youtube_transcript_api`
- Falls back to audio transcription using Whisper (`openai` SDK)
- Uses GPT models to generate structured summaries
- Supports output as:
  - Terminal printout
  - Markdown (`.md`)
  - Plain text (`.txt`)
- Handles missing tools (`yt-dlp`, `ffmpeg`) and API key validation gracefully
- Logs each step of the process with clear diagnostic output
- Enforces Whisper API file size limits (<25MB)

## Requirements

- Python 3.8+
- `yt-dlp` installed and available in `PATH`
- `ffmpeg` (for audio extraction and format conversion)
- OpenAI API key (GPT + Whisper access)

## Installation

git clone https://github.com/clorth0/gpt-video-summarizer.git
cd gpt-video-summarizer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Install external dependencies if not already available:

- macOS: `brew install ffmpeg yt-dlp`
- Debian/Ubuntu: `sudo apt install ffmpeg && pipx install yt-dlp`

Create a `.env` file with your OpenAI API key:

## Usage

Run the tool with a YouTube video ID (not the full URL):

python3 transcribe.py <youtube_video_id>

## Notes

- Videos longer than ~10 minutes may exceed the Whisper API 25MB size limit.
- Whisper is only used if the YouTube transcript is unavailable.
- `yt-dlp` must be in the system path; install via `brew`, `pipx`, or other.
- `ffmpeg` is required for audio extraction; install it via your OS package manager.
- Logging provides clear status and errors for debugging.

## License

MIT License. Contributions welcome.
