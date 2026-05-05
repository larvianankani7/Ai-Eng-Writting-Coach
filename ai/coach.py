import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY")
)
def review_text(text):
    prompt = f"""
    You are an expert English writing coach.
    Improve the following text:
    - fix grammar
    - improve clarity
    - make it more professional
    - keep meaning same

    Text:
    {text}
    """
    response = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",  # free/cheap option on OpenRouter
        messages=[
            {"role": "system", "content": "You are a helpful writing assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content