import openai
import os

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def complete_chat(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes YouTube transcripts."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=1000
    )
    return response['choices'][0]['message']['content'].strip()
