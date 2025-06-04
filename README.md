# GPT YouTube Video Summarizer (Updated)

This is a Python-based tool for extracting transcripts from YouTube videos and summarizing them using OpenAI's GPT models. The script leverages the YouTube Transcript API and OpenAI's `chat.completion` endpoint to provide structured summaries with a title, key bullet points, and a conclusion.

## Features

- Fetches YouTube video transcripts using `youtube_transcript_api`
- Generates structured summaries via GPT-3.5 or GPT-4
- Customizable prompt settings: temperature, max_tokens
- Secure API key handling with `.env` support
- CLI support via `argparse` for flexible usage
- Logging and error handling for robustness

## Requirements

- Python 3.8+
- OpenAI API key (stored in `.env` or exported as `OPENAI_API_KEY`)
- Required libraries:
  ```bash
  pip install openai youtube-transcript-api python-dotenv
  ```

## Usage

### Step 1: Set your OpenAI API Key

Create a `.env` file in the root directory:
```bash
OPENAI_API_KEY=your-api-key-here
```

### Step 2: Run the summarizer

```bash
python summarize.py <video_id>
```

#### Optional Arguments:
```bash
--max_tokens     Maximum tokens in the summary (default: 150)
--temperature    Sampling temperature for GPT (default: 0.7)
```

### Example
```bash
python summarize.py dQw4w9WgXcQ --max_tokens 300 --temperature 0.5
```

## Output

The output will be printed to the console in a structured format:

```
--- Video Summary ---

Title: Why Consistency Beats Talent

- Success is often the result of sustained effort, not raw skill
- Consistency leads to compounding progress over time
- People underestimate the power of showing up every day

Conclusion: This video argues that regular effort and discipline are more impactful than short bursts of brilliance.
```

## Development Notes

- Script modularized into:
  - `get_transcript(video_id)`
  - `generate_summary(transcript)`
- Uses OpenAI's `chat` API (recommended)
- Logging replaces print-based debugging
- Errors are logged with context (e.g. transcript issues, API failures)
- Summary prompt is hardcoded; customize by editing the `user_prompt` string inside `generate_summary()`

## License

MIT License. Contributions welcome.

---

Originally inspired by Daniel Miessler’s summarization tool. Maintained by @clorth0. Modernized for 2025 API usage.
