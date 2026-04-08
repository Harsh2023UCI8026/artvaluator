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
from openai import OpenAI
from env.art_env import ArtEnv, Action

# API client setup
client = OpenAI(
    base_url=os.getenv("API_BASE_URL"),
    api_key=os.getenv("HF_TOKEN")
)

def main():
    st.set_page_config(page_title="ArtValuator - Professional Evaluation", layout="centered")
    st.title("🎨 ArtValuator")
    st.write("Apni artwork ki sahi market value aur reach janne ke liye details bharein.")

    uploaded_file = st.file_uploader("Artwork upload karein", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        # Warning fix: use_column_width ki jagah width use kiya hai
        st.image(uploaded_file, caption="Uploaded Artwork", width=500)
        
        st.subheader("Artwork Details (Manual Input Required)")
        col1, col2 = st.columns(2)
        
        with col1:
            mat_cost = st.number_input("Material Cost (₹)", min_value=0.0, value=0.0, step=50.0)
            frame_cost = st.number_input("Frame Cost (₹)", min_value=0.0, value=0.0, step=50.0)
            time_spent = st.slider("Time Spent (Hours)", 1, 500, 5)
        
        with col2:
            size = st.selectbox("Size", ["small", "medium", "large"])
            surface = st.selectbox("Surface", ["canvas", "paper", "wood", "other"])
            detail_level = st.slider("Complexity/Detail (1-10)", 1, 10, 5)

        originality = st.slider("Originality Score (1-10)", 1, 10, 5)
        story_score = st.slider("Story/Narrative Depth (1-10)", 1, 10, 5)
        user_desc = st.text_area("Aapki initial description", placeholder="Painting ke baare mein kuch likhein...")

        if st.button("Run Full AI Evaluation"):
            with st.spinner("AI analysis chal rahi hai..."):
                # Data dictionary for environment
                data = {
                    "material_cost": mat_cost,
                    "frame_cost": frame_cost,
                    "time_spent": time_spent,
                    "size": size,
                    "surface_type": surface,
                    "detail_level": detail_level,
                    "originality": originality,
                    "story_score": story_score,
                    "user_description": user_desc
                }
                
                env = ArtEnv(data)
                
                # Medium Task: Refined Description using API
                prompt = f"Act as an art curator. Refine this description: '{user_desc}'. Data: Size {size}, Detail {detail_level}/10, Originality {originality}/10. Make it deep, emotional, and professional for an exhibition."
                
                response = client.chat.completions.create(
                    model=os.getenv("MODEL_NAME", "meta-llama/Llama-3-8B-Instruct"),
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=300
                )
                refined_desc = response.choices[0].message.content

                # Execute Environment step
                action = Action(predicted_price=0.0, description=refined_desc)
                obs, reward, done, info = env.step(action)
                
                st.success("Evaluation Complete!")

                # --- Task 1: Sales Strategy ---
                st.subheader("📍 Easy Task: Sales Strategy")
                st.info("Maine aapke liye ye platforms shortlist kiye hain:")
                
                # Focus on your personal website
                st.markdown(f"""
                **Primary Recommendation (Top Priority):**
                * **Sell-Buy-Artworks (My Personal Website):** [Visit Site](https://sell-buy-artworks.netlify.app/)
                  Is website ko maine khud design kiya hai. Aap yahan apni artwork showcase karne ke liye mujhe request bhej sakte hain. Audience aapka kaam explore kar payegi aur pasand aane par direct buy bhi kar sakti hai. Contact details website par di hui hain.
                
                **Other Online Platforms:**
                * **Saatchi Art:** International audience ke liye behtareen hai.
                * **Etsy:** Hand-made aur creative products ke liye global marketplace.
                * **Instagram Art:** Direct DM based sales ke liye.
                
                **Offline Options:**
                * **Local Art Galleries:** Physical networking ke liye best.
                * **Art Fairs/Exhibitions:** High-ticket clients se milne ke liye.
                """)
                st.write(f"Task Reward: {reward.value * 0.2:.4f}")

                # --- Task 2: AI Description ---
                st.subheader("📝 Medium Task: Refined AI Description")
                st.write(refined_desc)
                st.write(f"Task Reward: {reward.value * 0.3:.4f}")

                # --- Task 3: Pricing Analysis ---
                st.subheader("💰 Hard Task: Pricing Analysis")
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Predicted Market Value", f"₹{info['predicted_price']}")
                    st.caption("AI prediction based on quality and current trends.")
                with col_b:
                    st.metric("Actual Calculated Value", f"₹{info['actual_price']}")
                    st.caption("Base value calculated using labor, material, and uniqueness formula.")
                
                st.write(f"**Price Difference:** ₹{abs(info['predicted_price'] - info['actual_price'])}")
                st.write(f"Task Reward: {reward.value * 0.5:.4f}")

                # Total Reward
                st.divider()
                st.write(f"**Total Environment Reward Score:** {reward.value}")
                st.progress(reward.value)

if __name__ == "__main__":
    main()