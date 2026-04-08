# import streamlit as st
# from PIL import Image
# from utils.pricing import calculate_price, get_price_range
# from utils.validation import validate_all
# from models.image_model import is_artwork, extract_features
# from models.text_model import enhance_description_with_image
# from env.art_env import ArtEnv, Action
# from env.grader import grade_easy, grade_medium, grade_hard

# def main():
#     st.title("🎨 ArtValuator")
#     st.markdown("---")

#     uploaded = st.file_uploader("Upload artwork", type=["jpg", "png", "jpeg"])

#     if uploaded:
#         image = Image.open(uploaded).convert("RGB").resize((512, 512))
#         st.image(image, caption="Uploaded Artwork", use_column_width=True)

#         if not is_artwork(image):
#             st.error("The uploaded file does not appear to be a valid artwork.")
#             return

#         features = extract_features(image)
        
#         col1, col2 = st.columns(2)
#         with col1:
#             st.info(f"Detected Size: {features['size']}")
#         with col2:
#             st.info(f"Detail Level: {features['detail_level']}/10")

#         # Inputs
#         material = st.number_input("Material cost (₹)", min_value=0.0, value=100.0)
#         frame = st.number_input("Frame cost (₹)", min_value=0.0, value=50.0)
#         time = st.slider("Time Spent (hours)", 1, 100, 5)
#         originality = st.slider("Originality Score", 0, 10, 5)
#         story = st.slider("Story/Narrative Score", 0, 10, 5)
#         desc = st.text_area("Initial Description", placeholder="Briefly describe your inspiration...")

#         if st.button("🚀 Run Full AI Evaluation"):
#             data = {
#                 "material_cost": material,
#                 "frame_cost": frame,
#                 "time_spent": time,
#                 "size": features["size"],
#                 "surface_type": "canvas",
#                 "detail_level": features["detail_level"],
#                 "originality": originality,
#                 "story_score": story
#             }

#             valid, msg = validate_all(data, image)
#             if not valid:
#                 st.error(msg)
#                 return

#             # Logic
#             env = ArtEnv(data)
#             env.reset()
#             predicted_price = calculate_price(data)
            
#             # AI Description Enhancement
#             with st.spinner("AI analyzing visuals and text..."):
#                 improved_desc = enhance_description_with_image(image, desc, features["size"], features["detail_level"])

#             action = Action(predicted_price=predicted_price, description=improved_desc)
#             obs, reward, done, info = env.step(action)

#             # Results UI
#             st.success("Evaluation Complete!")
            
#             st.subheader("📍 Easy Task: Sales Strategy")
#             st.write("Recommended Platforms: Instagram, Etsy")
#             st.markdown("[Visit our Free Marketplace](https://sell-buy-artworks.netlify.app/)")

#             st.subheader("📝 Medium Task: AI Description")
#             st.write(improved_desc)

#             st.subheader("💰 Hard Task: Pricing Analysis")
#             min_p, max_p = get_price_range(predicted_price)
#             st.metric("Fair Market Value", f"₹{predicted_price}")
#             st.write(f"Negotiation Range: ₹{min_p} - ₹{max_p}")
            
#             st.subheader("🏆 Environment Rewards")
#             st.progress(reward.value)
#             st.write(f"Reward Score: {round(reward.value, 4)}")





import streamlit as st
import os
import google.generativeai as genai
from env.art_env import ArtEnv, Action

# 1. API Configuration
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# 2. Dynamic Model Selection (404 Error Fix)
def get_best_model():
    try:
        # Saare available models ki list check karein
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # Sabse behtar model chunein (Flash usually reliable hota hai)
        for m in models:
            if 'gemini-1.5-flash' in m:
                return m
        return models[0] # Fallback to first available model
    except Exception:
        return 'models/gemini-1.5-flash' # Manual default

active_model_name = get_best_model()
model = genai.GenerativeModel(active_model_name)

def main():
    st.set_page_config(page_title="ArtValuator Pro", layout="centered")
    st.title("🎨 ArtValuator")
    
    # User Inputs
    uploaded_file = st.file_uploader("Artwork upload karein", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        st.image(uploaded_file, caption="Aapki Artwork", width=500) 
        
        col1, col2 = st.columns(2)
        with col1:
            mat_cost = st.number_input("Material Cost (₹)", min_value=0.0, value=100.0)
            frame_cost = st.number_input("Frame Cost (₹)", min_value=0.0, value=50.0)
            work_hours = st.slider("Time Spent (Hours)", 1, 300, 5)
        
        with col2:
            uniqueness = st.slider("Originality Score", 1, 10, 5)
            story_depth = st.slider("Story Score", 1, 10, 5)
            complexity = st.slider("Detail Level", 1, 10, 3)

        raw_desc = st.text_area("Initial Description", value="painting of lord maa durga with 2 giant lions on canvas")

        if st.button("Run Full AI Evaluation"):
            if not api_key:
                st.error("GEMINI_API_KEY missing in Secrets.")
                return

            try:
                with st.spinner(f"Analyzing using {active_model_name}..."):
                    # Task Logic
                    prompt = f"Refine this art description professionally: '{raw_desc}'. Context: Detail {complexity}/10, Originality {uniqueness}/10."
                    response = model.generate_content(prompt)
                    final_description = response.text

                    # Environment Logic
                    env_data = {"mat": mat_cost, "frame": frame_cost, "time": work_hours, "orig": uniqueness, "story": story_depth, "detail": complexity}
                    env = ArtEnv(env_data)
                    action = Action(predicted_price=0.0, description=final_description)
                    _, reward, _, info = env.step(action)
                    
                    # Display Results
                    st.success("Evaluation Complete!")
                    st.subheader("📍 Sales Strategy (Easy)")
                    st.markdown(f"* **My Website:** [Sell-Buy-Artworks](https://sell-buy-artworks.netlify.app/)")
                    
                    st.subheader("📝 AI Description (Medium)")
                    st.write(final_description)

                    st.subheader("💰 Pricing Analysis (Hard)")
                    st.metric("Predicted Market Value", f"₹{info['pred']}")
                    st.metric("Actual Mathematical Value", f"₹{info['act']}")

            except Exception as e:
                st.error(f"Error logic failed: {e}")

if __name__ == "__main__":
    main()