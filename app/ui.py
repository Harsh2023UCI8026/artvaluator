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

# Gemini Configuration
# Ensure 'GEMINI_API_KEY' is set in Hugging Face Secrets
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

def main():
    st.set_page_config(page_title="ArtValuator Pro", layout="centered")
    st.title("🎨 ArtValuator")
    
    # Warning fix: updated width parameter
    uploaded_file = st.file_uploader("Artwork upload karein", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        st.image(uploaded_file, caption="Aapki Artwork", width=500) 
        
        st.subheader("Manual Specifications")
        col1, col2 = st.columns(2)
        with col1:
            mat_cost = st.number_input("Material Cost (₹)", min_value=0.0)
            frame_cost = st.number_input("Frame Cost (₹)", min_value=0.0)
            work_hours = st.slider("Time Spent (Hours)", 1, 300, 10)
        
        with col2:
            uniqueness = st.slider("Originality Score (1-10)", 1, 10, 5)
            story_depth = st.slider("Story Score (1-10)", 1, 10, 5)
            complexity = st.slider("Detail Level (1-10)", 1, 10, 5)

        raw_desc = st.text_area("Initial Description", placeholder="Painting ke bare mein likhein...")

        if st.button("Run Full AI Evaluation"):
            try:
                with st.spinner("Gemini AI analyzing..."):
                    # Medium Task: Refine Description using Gemini API
                    prompt = f"Refine this art description: '{raw_desc}'. Details: Complexity {complexity}/10, Originality {uniqueness}/10. Make it professional."
                    response = model.generate_content(prompt)
                    final_description = response.text

                    # Env calculation
                    env_data = {"material_cost": mat_cost, "frame_cost": frame_cost, "time_spent": work_hours, 
                                "originality": uniqueness, "story_score": story_depth, "detail_level": complexity}
                    
                    env = ArtEnv(env_data)
                    action = Action(predicted_price=0.0, description=final_description)
                    _, reward, _, info = env.step(action)
                    
                    st.success("Analysis Complete!")

                    # Easy Task: Platforms & Personal Website
                    st.subheader("📍 Easy Task: Sales Strategy")
                    st.info(f"Task Reward: {reward.value * 0.2:.4f}")
                    st.markdown(f"""
                    * **Sell-Buy-Artworks (My Website):** [Visit Site](https://sell-buy-artworks.netlify.app/)
                      **Note:** Is website ko maine khud banaya hai. Aap mujhe yahan request bhej sakte hain artwork upload karne ke liye. Audience aapka kaam dekh kar buy kar sakti hai.
                    * **Instagram/Etsy:** Global reach ke liye best platforms hain.
                    """)

                    # Medium Task Output
                    st.subheader("📝 Medium Task: AI Description")
                    st.info(f"Task Reward: {reward.value * 0.3:.4f}")
                    st.write(final_description)

                    # Hard Task Output
                    st.subheader("💰 Hard Task: Pricing Analysis")
                    st.info(f"Task Reward: {reward.value * 0.5:.4f}")
                    c1, c2 = st.columns(2)
                    c1.metric("Predicted Market Value", f"₹{info['predicted_price']}")
                    c2.metric("Actual Mathematical Value", f"₹{info['actual_price']}")
                    st.write(f"Difference: ₹{abs(info['predicted_price'] - info['actual_price'])}")

            except Exception as e:
                st.error(f"Error: {e}")
                st.info("Check karein ki kya 'GEMINI_API_KEY' sahi se set hai Settings mein.")

if __name__ == "__main__":
    main()