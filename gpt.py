import os
from openai import OpenAI

def summarize_transcript(transcript: str, title: str) -> str:
    """
    Summarizes a YouTube transcript using the OpenAI Chat API.

    The summary includes:
    - A one-line summary
    - 3–5 key points
    - 2–3 actionable steps
    - Any statistics or claims mentioned

    Returns:
        A structured summary string.
    Raises:
        RuntimeError: If the OpenAI API key is not set.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set. Check your .env file or environment.")

    # Allow optional model override (default to GPT-4)
    model = os.getenv("OPENAI_MODEL", "gpt-4")

    client = OpenAI(api_key=api_key)

    system_prompt = (
        "You are an expert summarizer. Summarize transcripts from educational YouTube videos into:\n"
        "- A one-line summary\n"
        "- 3–5 key points\n"
        "- 2–3 actionable steps\n"
        "- Any statistics or claims made\n"
        "Format clearly with headings."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Title: {title}\nTranscript:\n{transcript}"}
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
        max_tokens=800
    )

    return response.choices[0].message.content.strip()
