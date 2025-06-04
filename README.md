# GPT YouTube Video Summarizer (Updated)

This is a Python-based tool for extracting transcripts from YouTube videos and summarizing them using OpenAI's GPT models. The script leverages the YouTube Transcript API and OpenAI's `chat.completions` endpoint to provide structured summaries with a title, key bullet points, action steps, and any cited statistics.

## Features

- Fetches YouTube video transcripts using `youtube_transcript_api`
- Falls back to OpenAI Whisper API if transcript is unavailable
- Generates structured summaries using GPT-4 (or GPT-3.5)
- Real-time spinner progress during transcription
- Secure API key handling using `.env` or environment variables
- Modular and extensible Python script

## Requirements

- Python 3.8+
- OpenAI API key (set via `.env` or `OPENAI_API_KEY`)
- Required libraries:
  ```bash
  pip install openai youtube-transcript-api pytube yt-dlp python-dotenv
  ```
- `ffmpeg` for audio processing (required by `yt-dlp`)
  ```bash
  brew install ffmpeg  # macOS
  sudo apt install ffmpeg  # Ubuntu/Debian
  ```

## Usage

### Step 1: Set your OpenAI API Key

Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your-api-key-here
```
Or export it directly:
```bash
export OPENAI_API_KEY=your-api-key-here
```

### Step 2: Run the summarizer

```bash
python transcribe.py <video_id>
```

### Example
```bash
python transcribe.py dQw4w9WgXcQ
```

## Output

The output will be printed to the console in a structured format:

```
--- Structured Summary ---

Summary:
This video discusses how sustained effort beats innate talent over the long term.

Key Points:
- Daily practice outperforms occasional bursts of brilliance
- Talent without consistency leads to stagnation
- Routine creates long-term momentum

Actionable Steps:
- Set small, repeatable goals
- Focus on showing up every day
- Track progress over time

Statistics or Claims:
- Referenced the “10,000-hour rule” as a benchmark for mastery
```

## Development Notes

- Modular structure:
  - `get_transcript(video_id)` — fetch from YouTube
  - `download_audio(video_id)` + `transcribe_whisper()` — fallback
  - `summarize(transcript, title)` — GPT-powered summary
- Uses OpenAI Python SDK v1.x (latest)
- Spinner indicates processing during Whisper API calls
- Structured prompt improves clarity of output
- Errors are logged clearly for diagnosis

## License

MIT License. Contributions welcome.

---

Originally inspired by Daniel Miessler’s summarization tool. Maintained by Matt James. Modernized for 2025 API usage.
