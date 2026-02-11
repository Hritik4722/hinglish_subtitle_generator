import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.types import Schema, Type

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "gemini-2.5-flash"

def convert_hinglish(segments):
    texts = [seg["text"] for seg in segments]

    
    prompt = f"""
        You are a professional subtitle editor.

        The following sentences are rough speech-to-text outputs.
        They may contain spelling mistakes or incorrect Hindi words.

        Your task:
        1. Correct the meaning.
        2. Convert everything into natural Hinglish.
        3. Transliterate Hindi words into English letters
        4. Use English letters only.
        5. Use numerals for any number text
        6. Keep sentence count SAME as input.
        
        SENTENCES:
        {json.dumps(texts, ensure_ascii=False)}

        Return ONLY a JSON array of corrected sentences.
        Do NOT translate Hindi words into English language
        Do NOT add explanations.
        Do not add markdown.
        Do not explain.
                
    """

 

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type= "application/json",
            response_schema= {
                "type": "array",
                "items": {
                    "type": "string"
                }
            },
            temperature=0.3
        )
    )

    cleaned_text = response.parsed

    for i in range(len(segments)):
        segments[i]["text"] = cleaned_text[i]

    return segments
