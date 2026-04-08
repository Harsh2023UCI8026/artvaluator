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

# API client configuration
# Make sure HF_TOKEN and API_BASE_URL are set in Hugging Face Secrets
client = OpenAI(
    base_url=os.environ.get("API_BASE_URL"),
    api_key=os.environ.get("HF_TOKEN")
)

def main():
    st.set_page_config(page_title="ArtValuator | Professional Art Analysis", layout="centered")
    st.title("🎨 ArtValuator")
    st.write("Professional tools se apni artwork ka sahi mulyankan karein.")

    # File uploader
    artwork_file = st.file_uploader("Apni artwork ki image yahan upload karein", type=["jpg", "png", "jpeg"])

    if artwork_file:
        # Warning fix: updated use_column_width to width
        st.image(artwork_file, caption="Aapki Uploaded Artwork", width=500)
        
        st.subheader("Manual Specifications")
        st.write("Sahi results ke liye niche diye gaye fields ko khud bharein:")
        
        col1, col2 = st.columns(2)
        with col1:
            mat_cost = st.number_input("Materials par kharch (₹)", min_value=0.0, step=10.0)
            frame_cost = st.number_input("Framing ka kharch (₹)", min_value=0.0, step=10.0)
            work_hours = st.slider("Kitne ghante kaam kiya?", 1, 300, 10)
        
        with col2:
            canvas_size = st.selectbox("Painting ka size", ["small", "medium", "large"])
            art_surface = st.selectbox("Surface type", ["canvas", "paper", "wood", "digital"])
            complexity = st.slider("Complexity level (1-10)", 1, 10, 5)

        # Intangible values
        uniqueness = st.slider("Originality Score", 1, 10, 5)
        story_depth = st.slider("Story/Narrative Score", 1, 10, 5)
        raw_desc = st.text_area("Initial Description", placeholder="Artwork ke baare mein kuch shabd likhein...")

        if st.button("Run Full AI Evaluation"):
            try:
                with st.spinner("AI aapki artwork ko analyze kar raha hai..."):
                    # Prepare data for Environment
                    env_input = {
                        "material_cost": mat_cost,
                        "frame_cost": frame_cost,
                        "time_spent": work_hours,
                        "size": canvas_size,
                        "surface_type": art_surface,
                        "detail_level": complexity,
                        "originality": uniqueness,
                        "story_score": story_depth
                    }
                    
                    env = ArtEnv(env_input)
                    
                    # Refine Description using LLM
                    art_prompt = f"Develop a deep, emotional curatorial description for this artwork. Base info: {raw_desc}. Details: {canvas_size} {art_surface}, detail level {complexity}/10, and high originality. Highlight the soul of the work."
                    
                    ai_response = client.chat.completions.create(
                        model=os.environ.get("MODEL_NAME", "meta-llama/Llama-3-8B-Instruct"),
                        messages=[{"role": "user", "content": art_prompt}],
                        max_tokens=400
                    )
                    final_description = ai_response.choices[0].message.content

                    # Run env step
                    action = Action(predicted_price=0.0, description=final_description)
                    obs, reward, done, info = env.step(action)
                    
                    st.success("Analysis Poori Ho Gayi!")

                    # TASK 1: Sales Strategy
                    st.markdown("### 📍 Easy Task: Sales Strategy & Reach")
                    st.info("Aapke liye best recommended platforms:")
                    st.markdown(f"""
                    * **Sell-Buy-Artworks (My Portfolio Website):** [Visit Site](https://sell-buy-artworks.netlify.app/)
                      **Personal Note:** Is website ko maine khud banaya hai. Aap yahan apni artwork upload karne ke liye mujhe request bhej sakte hain. Ye platform meri audience ke liye hai jahan log aapki art explore aur buy kar sakte hain. Contact number website par available hai!
                    * **Instagram & Pinterest:** Visual reach ke liye best offline-online mix.
                    * **Etsy:** Agar aap international shipping ke liye ready hain.
                    """)
                    st.write(f"Task Reward: {reward.value * 0.2:.2f}")

                    # TASK 2: AI Description
                    st.markdown("### 📝 Medium Task: Refined Exhibition Description")
                    st.write(final_description)
                    st.write(f"Task Reward: {reward.value * 0.3:.2f}")

                    # TASK 3: Pricing Analysis
                    st.markdown("### 💰 Hard Task: Financial Valuation")
                    col_p, col_a = st.columns(2)
                    with col_p:
                        st.metric("Predicted Market Value", f"₹{info['predicted_price']}")
                        st.caption("AI based emotional and demand value.")
                    with col_a:
                        st.metric("Actual Mathematical Value", f"₹{info['actual_price']}")
                        st.caption("Cost + Labor + Skill based valuation.")
                    
                    st.markdown(f"**Valuation Logic:** Actual price aapke mehnat aur material cost ko skill factor se multiply karke nikali gayi hai. Predicted price market demand aur aapki story ke emotional weight par nirbhar hai.")
                    st.write(f"Task Reward: {reward.value * 0.5:.2f}")

                    # Final Reward Score
                    st.divider()
                    st.write(f"**Environment Reward Summary:** {reward.value}")
                    st.progress(reward.value)

            except Exception as e:
                st.error(f"Error: {e}")
                st.write("Check karein ki kya 'HF_TOKEN' sahi se set hai Settings mein.")

if __name__ == "__main__":
    main()