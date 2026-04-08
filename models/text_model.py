import os

API_KEY = os.environ.get("GEMINI_API_KEY")

# -------------------------------
# SAFE FALLBACK
# -------------------------------
def fallback_response(description, size, detail):
    return f"""
This artwork shows a beautiful composition.

Description: {description}
Size: {size}
Detail level: {detail}/10

The artwork expresses emotions and creativity.
It can attract buyers due to its uniqueness and effort.
"""

# -------------------------------
# MAIN FUNCTION
# -------------------------------
def enhance_description_with_image(image, description, size, detail):

    if not API_KEY:
        return "⚠️ Gemini API key not found."

    try:
        import google.generativeai as genai
        genai.configure(api_key=API_KEY)

        image = image.convert("RGB")

        prompt = f"""
Describe this artwork emotionally.

Description: {description}
Size: {size}
Detail level: {detail}/10
"""

        model = genai.GenerativeModel("gemini-pro")  # ✅ TEXT ONLY (STABLE)

        response = model.generate_content(prompt)

        return response.text if response.text else fallback_response(description, size, detail)

    except Exception as e:
        return fallback_response(description, size, detail)