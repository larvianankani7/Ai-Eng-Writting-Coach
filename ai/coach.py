import os
import json
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
Return ONLY valid JSON. No explanation. No markdown.
Format:
{{
  "corrected_text": "string",
  "grammar_errors": [],
  "suggestions": [],
  "tone": "formal/casual/neutral",
  "score": 0,
  "summary": "string"
}}
Text:
{text}
"""
    response = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You only return valid JSON."},
            {"role": "user", "content": prompt}
        ]
    )
    content = response.choices[0].message.content
    if content is None:
        return {
            "corrected_text": "",
            "grammar_errors": [],
            "suggestions": [],
            "tone": "unknown",
            "score": 0,
            "summary": "Empty response from model"
        }
    content = str(content)
    content = content.strip()
    content = content.replace("json", "").replace("", "")
    start = content.find("{")
    end = content.rfind("}")
    if start != -1 and end != -1:
        content = content[start:end+1]
    try:
        return json.loads(content)
    except Exception as e:
        return {
            "corrected_text": content,
            "grammar_errors": [],
            "suggestions": [],
            "tone": "unknown",
            "score": 0,
            "summary": f"Parsing failed: {str(e)}"
        }