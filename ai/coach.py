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
You are a professional English writing coach.

Your job is to analyze the GIVEN TEXT ONLY.

Do NOT give generic answers.
Do NOT repeat same suggestions.
Base everything strictly on the input text.

Return ONLY valid JSON:

{{
  "corrected_text": "...",
  "grammar_errors": ["specific mistakes found in THIS text"],
  "suggestions": ["specific improvements based on THIS text"],
  "tone": "formal / casual / neutral",
  "score": 0-100,
  "summary": "short feedback based on THIS text"
}}

IMPORTANT RULES:
- If text is good → say "no major issues"
- If text is bad → point exact errors
- DO NOT hallucinate problems
- Be strict and accurate

TEXT:
{text}
"""
    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        temperature=0.3,
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