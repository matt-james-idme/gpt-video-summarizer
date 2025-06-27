import os
from openai import OpenAI, RateLimitError, APIError, OpenAIError

def truncate_text(text, max_tokens=6000):
    """Rough truncation based on ~4 characters per token."""
    return text[:max_tokens * 4]

def summarize_transcript(transcript: str, title: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set. Check your .env file or environment.")

    preferred_model = os.getenv("OPENAI_MODEL", "gpt-4")
    fallback_model = "gpt-3.5-turbo"
    client = OpenAI(api_key=api_key)

    transcript = truncate_text(transcript)

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

    def try_model(model_name):
        return client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=0.7,
            max_tokens=800
        )

    try:
        return try_model(preferred_model).choices[0].message.content.strip()
    except RateLimitError as e:
        print(f"[ERROR] Rate limit or token limit exceeded for model '{preferred_model}'.")
        print("Trying fallback model 'gpt-3.5-turbo'...")

        try:
            return try_model(fallback_model).choices[0].message.content.strip()
        except Exception as fallback_error:
            raise RuntimeError(f"Both models failed due to rate limits or input size. {fallback_error}")
    except OpenAIError as e:
        raise RuntimeError(f"OpenAI API error occurred: {e}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error during summarization: {e}")
