import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_transcript(transcript: str, title: str) -> str:
    system_prompt = (
        "You are an expert summarizer. Summarize transcripts from educational YouTube videos into:"
        "\n- A one-line summary"
        "\n- 3–5 key points"
        "\n- 2–3 actionable steps"
        "\n- Any statistics or claims made"
        "\nFormat clearly with headings."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Title: {title}\nTranscript:\n{transcript}"}
    ]

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7,
        max_tokens=800
    )

    return response.choices[0].message.content.strip()
