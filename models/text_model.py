# models/text_model.py

import os

# -------------------------------
# LOAD API KEY
# -------------------------------
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    def enhance_description_with_image(image, description, size, detail):
        return "⚠️ Gemini API key not found. Add it in HF Secrets."
else:
    try:
        from google import genai

        client = genai.Client(api_key=API_KEY)

    except Exception as e:
        def enhance_description_with_image(image, description, size, detail):
            return f"Import Error: {str(e)}"

    else:
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
                    contents=[prompt, image]
                )

                return response.text.strip()

            except Exception as e:
                return f"Gemini Error: {str(e)}"