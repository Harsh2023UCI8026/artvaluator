import streamlit as st
from PIL import Image
from utils.pricing import calculate_price, get_price_range
from utils.validation import validate_all
from models.image_model import is_artwork, extract_features
from models.text_model import enhance_description_with_image
from env.art_env import ArtEnv, Action
from env.grader import grade_easy, grade_medium, grade_hard

def main():
    st.title("🎨 ArtValuator")
    st.markdown("---")

    uploaded = st.file_uploader("Upload artwork", type=["jpg", "png", "jpeg"])

    if uploaded:
        image = Image.open(uploaded).convert("RGB").resize((512, 512))
        st.image(image, caption="Uploaded Artwork", use_column_width=True)

        if not is_artwork(image):
            st.error("The uploaded file does not appear to be a valid artwork.")
            return

        features = extract_features(image)
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"Detected Size: {features['size']}")
        with col2:
            st.info(f"Detail Level: {features['detail_level']}/10")

        # Inputs
        material = st.number_input("Material cost (₹)", min_value=0.0, value=100.0)
        frame = st.number_input("Frame cost (₹)", min_value=0.0, value=50.0)
        time = st.slider("Time Spent (hours)", 1, 100, 5)
        originality = st.slider("Originality Score", 0, 10, 5)
        story = st.slider("Story/Narrative Score", 0, 10, 5)
        desc = st.text_area("Initial Description", placeholder="Briefly describe your inspiration...")

        if st.button("🚀 Run Full AI Evaluation"):
            data = {
                "material_cost": material,
                "frame_cost": frame,
                "time_spent": time,
                "size": features["size"],
                "surface_type": "canvas",
                "detail_level": features["detail_level"],
                "originality": originality,
                "story_score": story
            }

            valid, msg = validate_all(data, image)
            if not valid:
                st.error(msg)
                return

            # Logic
            env = ArtEnv(data)
            env.reset()
            predicted_price = calculate_price(data)
            
            # AI Description Enhancement
            with st.spinner("AI analyzing visuals and text..."):
                improved_desc = enhance_description_with_image(image, desc, features["size"], features["detail_level"])

            action = Action(predicted_price=predicted_price, description=improved_desc)
            obs, reward, done, info = env.step(action)

            # Results UI
            st.success("Evaluation Complete!")
            
            st.subheader("📍 Easy Task: Sales Strategy")
            st.write("Recommended Platforms: Instagram, Etsy")
            st.markdown("[Visit our Free Marketplace](https://sell-buy-artworks.netlify.app/)")

            st.subheader("📝 Medium Task: AI Description")
            st.write(improved_desc)

            st.subheader("💰 Hard Task: Pricing Analysis")
            min_p, max_p = get_price_range(predicted_price)
            st.metric("Fair Market Value", f"₹{predicted_price}")
            st.write(f"Negotiation Range: ₹{min_p} - ₹{max_p}")
            
            st.subheader("🏆 Environment Rewards")
            st.progress(reward.value)
            st.write(f"Reward Score: {round(reward.value, 4)}")