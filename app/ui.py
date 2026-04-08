import streamlit as st
import os
import google.generativeai as genai
from env.art_env import ArtEnv, Action

# API Setup - Key hamesha Secrets se hi aayegi
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Stable model selection logic to avoid 404/403
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    model = genai.GenerativeModel('models/gemini-1.5-flash')

def main():
    st.set_page_config(page_title="ArtValuator Pro", layout="wide")
    st.title("🎨 ArtValuator")
    st.write("Professional Art Evaluation & Marketplace Strategy")

    uploaded_file = st.file_uploader("Artwork upload karein", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Artwork", width=500)
        
        # User Input Section
        st.subheader("📊 Art Specifications")
        col1, col2 = st.columns(2)
        
        with col1:
            mat_cost = st.number_input("Material Cost (₹)", min_value=0.0, value=100.0)
            frame_cost = st.number_input("Frame Cost (₹)", min_value=0.0, value=50.0)
            work_hours = st.slider("Time Spent (Hours)", 1, 300, 5)
        
        with col2:
            uniqueness = st.slider("Originality Score", 1, 10, 5)
            story_depth = st.slider("Story/Narrative Score", 1, 10, 5)
            complexity = st.slider("Detail Level", 1, 10, 3)

        raw_desc = st.text_area("Initial Description", value="painting of lord maa durga with 2 giant lions on canvas")

        if st.button("🚀 Run Full AI Evaluation"):
            if not api_key:
                st.error("Error: GEMINI_API_KEY settings mein nahi mili!")
                return

            try:
                with st.spinner("AI is analyzing your masterpiece..."):
                    # 1. Medium Task: AI Description Refinement
                    prompt = (f"Refine this art description professionally for an exhibition: '{raw_desc}'. "
                             f"Technical details: Detail level {complexity}/10, Originality {uniqueness}/10.")
                    response = model.generate_content(prompt)
                    refined_desc = response.text

                    # 2. Environment Logic (Linking to env/art_env.py)
                    env_data = {
                        "mat": mat_cost, "frame": frame_cost, "time": work_hours,
                        "orig": uniqueness, "story": story_depth, "detail": complexity
                    }
                    env = ArtEnv(env_data)
                    # Pricing logic calculations
                    action = Action(predicted_price=0.0, description=refined_desc)
                    _, reward, _, info = env.step(action)

                    st.success("Evaluation Complete!")
                    st.divider()

                    # --- EASY TASK: SALES STRATEGY ---
                    st.subheader("📍 Easy Task: Sales Strategy")
                    st.info(f"Task Reward: {reward.value * 0.2:.4f}")
                    st.markdown(f"""
                    * **Sell-Buy-Artworks (Personal Website):** [Visit Site](https://sell-buy-artworks.netlify.app/)
                        *Note: Is website ko maine design kiya hai. Aap yahan upload ke liye request bhej sakte hain.*
                    * **Global Recommendation:** Instagram Art community aur Etsy par focus karein.
                    """)

                    # --- MEDIUM TASK: AI DESCRIPTION ---
                    st.subheader("📝 Medium Task: Curated AI Description")
                    st.info(f"Task Reward: {reward.value * 0.3:.4f}")
                    st.write(refined_desc)

                    # --- HARD TASK: PRICING ANALYSIS ---
                    st.subheader("💰 Hard Task: Pricing Analysis")
                    st.info(f"Task Reward: {reward.value * 0.5:.4f}")
                    
                    c1, c2 = st.columns(2)
                    c1.metric("Predicted Market Value", f"₹{info['pred']}")
                    c2.metric("Actual Mathematical Value", f"₹{info['act']}")
                    
                    st.write(f"**Valuation logic:** Actual price material aur mehnat par hai, jabki Predicted price originality aur story score par depend karti hai.")

                    # --- OVERALL REWARD ---
                    st.subheader("🏆 Environment Rewards")
                    st.progress(reward.value)
                    st.write(f"Total Combined Reward Score: **{reward.value}**")

            except Exception as e:
                st.error(f"Error logic failed: {e}")
                st.info("Tip: Naya Project banakar API key replace karein.")

if __name__ == "__main__":
    main()