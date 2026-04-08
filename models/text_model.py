# models/text_model.py

import os
from google import genai

# -------------------------------
# LOAD ENV (SAFE FOR HF + LOCAL)
# -------------------------------
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

API_KEY = os.getenv("GEMINI_API_KEY")

# -------------------------------
# CLIENT INIT (SAFE)
# -------------------------------
client = None

if API_KEY:
    try:
        client = genai.Client(api_key=API_KEY)
    except Exception as e:
        client = None


# -------------------------------
# MAIN FUNCTION
# -------------------------------
def enhance_description_with_image(image, description, size, detail):

    # ❌ If no API key
    if not client:
        return "⚠️ Gemini API key not found. Please add it in HF Secrets."

    try:
        # Resize for performance (VERY IMPORTANT 🔥)
        image = image.convert("RGB").resize((512, 512))

        prompt = f"""
You are an expert art storyteller.

The user created this artwork.

User description: {description}
Size: {size}
Detail level: {detail}/10

Analyze BOTH the image and description carefully.

Write a beautiful caption that:
- explains what is happening in the painting
- describes emotions
- tells a meaningful story
- helps audience connect deeply
- makes buyers interested

Use simple English.
Make it emotional, human-like, and expressive.
Avoid generic lines.
Write at least 6–8 lines.
"""

        # ✅ Gemini call (UPDATED FORMAT)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[prompt, image]
        )

        # -------------------------------
        # SAFE RESPONSE EXTRACTION
        # -------------------------------
        if hasattr(response, "text") and response.text:
            return response.text.strip()

        if hasattr(response, "candidates"):
            try:
                return response.candidates[0].content.parts[0].text.strip()
            except:
                pass

        return "⚠️ AI returned empty response"

    except Exception as e:
        return f"⚠️ Gemini Error: {str(e)}"