# GPT Video Summarizer

This is a Python-based command-line tool for extracting transcripts from YouTube videos and generating structured summaries using OpenAI's GPT models. It first attempts to retrieve transcripts via the YouTube Transcript API, then falls back to audio transcription using the OpenAI Whisper API if necessary.

## Features

- Extracts YouTube transcripts using `youtube_transcript_api`
- Falls back to Whisper transcription via OpenAI API if transcript is unavailable
- Summarizes content using GPT-4 (or GPT-3.5 as a fallback)
- Outputs summary in structured format: summary, key points, actions, and statistics
- Prompts user to choose output format: terminal, `.md`, or `.txt`
- Secure API key handling via `.env` file
- Clear logging for each step and failure mode

## Requirements

- Python 3.8 or higher
- `ffmpeg` (required by `yt-dlp` for audio extraction)
- An OpenAI API key

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/clorth0/gpt-video-summarizer.git
   cd gpt-video-summarizer
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install `ffmpeg` if not already installed:
   - macOS: `brew install ffmpeg`
   - Ubuntu/Debian: `sudo apt install ffmpeg`

5. Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your-openai-api-key
   ```

## Usage

Run the script using a YouTube video ID (not the full URL):

```bash
python transcribe.py <video_id>
```

Example:

```bash
python transcribe.py dQw4w9WgXcQ
```

You will be prompted to choose an output format:

```
Choose output format:
1. Print to terminal
2. Save as Markdown (.md)
3. Save as Plain Text (.txt)
Enter 1, 2, or 3:
```

## Output Format

Summaries include the following structure:

- One-line summary
- 3–5 key points
- 2–3 actionable steps
- Any statistics or claims mentioned

Markdown and text outputs are saved in the current working directory, named according to the video ID.

## Project Structure

- `transcribe.py`: Main CLI script
- `gpt.py`: Handles summarization logic via OpenAI API
- `requirements.txt`: Python dependencies
- `.env`: Stores OpenAI API key (excluded from version control)

## Notes

- You must have a valid OpenAI API key with access to the GPT and Whisper APIs.
- This tool is designed for personal or research use; review OpenAI’s terms of service for usage constraints.
- Ensure that `yt-dlp` and `ffmpeg` are functioning correctly in your environment.

## License

MIT License. Contributions welcome.
