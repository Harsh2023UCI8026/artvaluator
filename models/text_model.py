# models/text_model.py

import os
import io
from dotenv import load_dotenv
from google import genai

# -------------------------------
# LOAD ENV
# -------------------------------
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

# safety check
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# initialize client (only once)
client = genai.Client(api_key=API_KEY)



# -------------------------------
# MAIN FUNCTION (IMAGE + AI)
# -------------------------------
def enhance_description_with_image(image, description, size, detail):

    try:
        image = image.convert("RGB")

        prompt = f"""
You are an expert art storyteller.

User description: {description}
Size: {size}
Detail level: {detail}/10

Analyze the image and explain:
- what is happening
- emotions
- story
- why buyer will like it

Use simple English. Make it emotional and detailed.
Write at least 6 lines.
"""

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[prompt, image]   # ✅ IMPORTANT CHANGE
        )

        # ✅ SAFE RESPONSE EXTRACTION
        if hasattr(response, "text") and response.text:
            return response.text.strip()

        # fallback extraction
        if hasattr(response, "candidates"):
            try:
                return response.candidates[0].content.parts[0].text.strip()
            except:
                pass

        return "AI returned empty response"

    except Exception as e:
        return f"Gemini Error: {str(e)}"