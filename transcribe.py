import os
import openai
from youtube_transcript_api import YouTubeTranscriptApi

openai.api_key = os.getenv('OPENAI_API_KEY')

def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_transcript = " ".join([seg['text'] for seg in transcript])
        return full_transcript
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def extract_video_summary_from_chunk(chunk, max_tokens=2000):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides a video summary."},
                {"role": "user", "content": f"Provide a summary of the following video:\n{chunk}\n\n[Please provide context or a brief description of the video's topic to assist in generating a summary.]"},
            ],
            max_tokens=max_tokens,
            temperature=0.7,
            stop=["\n"]  # Stop on newlines to capture complete sentences
        )
        
        # Extract the generated summary
        summary = response['choices'][0]['message']['content'].strip()
        
        return summary
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def extract_video_summary(text, max_tokens=2000):
    try:
        # Split the text into manageable chunks
        chunks = [text[i:i+max_tokens] for i in range(0, len(text), max_tokens)]

        video_summary = ""

        for chunk in chunks:
            chunk_summary = extract_video_summary_from_chunk(chunk, max_tokens)
            video_summary += chunk_summary + " "

        return video_summary
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def extract_major_themes(text, max_tokens=2000, target_takeaways=10):
    try:
        # Split the text into manageable chunks
        chunks = [text[i:i+max_tokens] for i in range(0, len(text), max_tokens)]

        major_themes = set()  # To ensure uniqueness

        for chunk in chunks:
            chunk_summary = extract_video_summary_from_chunk(chunk, max_tokens)
            major_themes.add(chunk_summary)

            if len(major_themes) >= target_takeaways:
                break

        return list(major_themes)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

if __name__ == "__main__":
    video_id = input("Enter YouTube Video ID: ")

    transcript = get_transcript(video_id)
    if transcript:
        video_summary = extract_video_summary(transcript)
        if video_summary:
            print("\nVideo Summary:")
            print(video_summary)

        major_themes = extract_major_themes(transcript)
        if major_themes:
            print("\nMajor Themes and Points:")
            for i, theme in enumerate(major_themes, start=1):
                print(f"{i}. {theme}")
