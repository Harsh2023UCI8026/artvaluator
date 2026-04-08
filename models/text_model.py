# models/text_model.py

import os

# ❌ dotenv remove (HF me needed nahi)
# from dotenv import load_dotenv
# load_dotenv()

# ✅ direct environment variable read
API_KEY = os.environ.get("GEMINI_API_KEY")

# -------------------------------
# SAFETY CHECK
# -------------------------------
if not API_KEY:
    def enhance_description_with_image(image, description, size, detail):
        return "⚠️ Gemini API key not found. Please add it in HF Secrets."
else:
    try:
        import google.generativeai as genai

        genai.configure(api_key=API_KEY)

    except Exception as e:
        def enhance_description_with_image(image, description, size, detail):
            return f"Gemini import error: {str(e)}"

    else:
        # -------------------------------
        # MAIN FUNCTION
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

                response = genai.GenerativeModel("gemini-1.5-flash").generate_content(
                    [prompt, image]
                )

                return response.text.strip()

            except Exception as e:
                return f"Gemini Error: {str(e)}"