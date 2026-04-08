# app/ui.py

import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from PIL import Image

from utils.pricing import calculate_price, get_price_range
from utils.validation import validate_all

from models.image_model import is_artwork, extract_features
from models.text_model import enhance_description_with_image

from env.art_env import ArtEnv, Action
from env.grader import grade_easy, grade_medium, grade_hard


st.set_page_config(page_title="ArtValuator")

st.title("ArtValuator")

uploaded = st.file_uploader("Upload artwork", type=["jpg","png","jpeg"])

if uploaded:

    image = Image.open(uploaded).resize((512,512))
    st.image(image)

    if not is_artwork(image):
        st.error("Not a valid artwork")
        st.stop()

    features = extract_features(image)

    st.write("Detected Size:", features["size"])
    st.write("Detail Level:", features["detail_level"])

    material = st.number_input("Material cost")
    frame = st.number_input("Frame cost")
    time = st.slider("Time",1,100)
    originality = st.slider("Originality",0,10)
    story = st.slider("Story",0,10)

    desc = st.text_area("Description")

    if st.button("Run Full Evaluation"):

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
            st.stop()

        env = ArtEnv(data)
        env.reset()

        predicted_price = calculate_price(data)

        action = Action(predicted_price=predicted_price, description=desc)

        obs, reward, done, info = env.step(action)

        # EASY TASK
        st.subheader("Easy Task: Where to Sell")
        platforms = ["Instagram", "Etsy"]

        st.write("Instagram: https://instagram.com")
        st.write("Etsy: https://etsy.com")
        st.write("Your platform: https://sell-buy-artworks.netlify.app/")

        # MEDIUM TASK
        st.subheader("Medium Task: Description")

        with st.spinner("AI is analyzing your artwork..."):
            improved = enhance_description_with_image(
                image, desc, features["size"], features["detail_level"]
            )

        st.write(improved)

        # HARD TASK
        st.subheader("Hard Task: Pricing")

        min_p, max_p = get_price_range(predicted_price)

        st.write("Predicted Price:", predicted_price)
        st.write("True Price:", env.true_price)
        st.write("Range:", min_p, "-", max_p)

        st.write("Factors:", info["factors"])

        # REWARD
        st.subheader("Reward System")

        st.write("Error:", info["error"])
        st.write("Reward:", reward.value)

        # GRADER
        easy_score = grade_easy(platforms)
        medium_score = grade_medium(improved)
        hard_score = grade_hard(predicted_price, env.true_price)

        final = (easy_score + medium_score + hard_score) / 3

        st.subheader("Final Score")
        st.write(final)
        st.progress(final)