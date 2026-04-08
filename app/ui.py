import streamlit as st
import os
import requests
import json
from env.art_env import ArtEnv, Action

# API Configuration - Isse manual error nahi aayega
api_key = os.environ.get("GEMINI_API_KEY")

def get_ai_analysis(prompt):
    """Direct REST call taaki 404/403 issues na aayein"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    return "Description refinement currently unavailable, but pricing logic is ready."

def main():
    st.set_page_config(page_title="ArtValuator Pro", layout="centered")
    st.title("🎨 ArtValuator")
    st.write("Professional Evaluation & Strategy Environment")

    uploaded_file = st.file_uploader("Artwork upload karein", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        # Fixed width parameter to avoid deprecation warning
        st.image(uploaded_file, caption="Aapki Artwork", width=500)
        
        st.subheader("Manual Data Inputs")
        st.write("Please provide the following details for evaluation:")
        
        col1, col2 = st.columns(2)
        with col1:
            mat_cost = st.number_input("Material & Framing Cost (₹)", min_value=0.0, value=500.0)
            work_hours = st.slider("Kitne ghante kaam kiya?", 1, 500, 15)
            detail_level = st.slider("Complexity (1-10)", 1, 10, 5)
        
        with col2:
            originality = st.slider("Originality (1-10)", 1, 10, 7)
            story_depth = st.slider("Story Narrative (1-10)", 1, 10, 6)
            surface = st.selectbox("Surface Type", ["Canvas", "Paper", "Digital", "Wood"])

        user_desc = st.text_area("Initial Description", placeholder="Artwork ke peeche ki kahani likhein...")

        if st.button("🚀 Run Full Evaluation"):
            if not api_key:
                st.error("API Key missing! Please add GEMINI_API_KEY to Secrets.")
                return

            with st.spinner("Analyzing environment..."):
                # Task 2: Description (Medium Task)
                prompt = f"Professionalize this art description: '{user_desc}'. Context: Detail level {detail_level}/10, Originality {originality}/10."
                refined_desc = get_ai_analysis(prompt)

                # Environment Step
                env_data = {"mat": mat_cost, "time": work_hours, "orig": originality, "story": story_depth, "detail": detail_level}
                env = ArtEnv(env_data)
                _, reward, _, info = env.step(Action(predicted_price=0.0, description=refined_desc))

                st.success("Evaluation Success!")

                # --- EASY TASK: Sales Strategy ---
                st.markdown("### 📍 Easy Task: Platform Recommendations")
                st.info(f"Task Reward: {reward.value * 0.2:.4f}")
                st.markdown(f"""
                * **Sell-Buy-Artworks (Recommended):** [Visit Site](https://sell-buy-artworks.netlify.app/)
                  **Personal Note:** Is website ko maine (developer) khud banaya hai. Aap yahan apni artwork upload karne ke liye request bhej sakte hain. Audience yahan artwork explore aur buy kar sakti hai. Contact details site par maujood hain.
                * **Behance/Instagram:** Portfolio showcase ke liye best hai.
                """)

                # --- MEDIUM TASK: AI Description ---
                st.markdown("### 📝 Medium Task: Refined Description")
                st.info(f"Task Reward: {reward.value * 0.3:.4f}")
                st.write(refined_desc)

                # --- HARD TASK: Pricing Analysis ---
                st.markdown("### 💰 Hard Task: Market Valuation")
                st.info(f"Task Reward: {reward.value * 0.5:.4f}")
                c1, c2 = st.columns(2)
                c1.metric("Predicted Market Value", f"₹{info['pred']}")
                c2.metric("Actual Mathematical Value", f"₹{info['act']}")
                
                st.write(f"**Difference:** ₹{abs(info['pred'] - info['act'])}")
                st.write("**Justification:** Actual value material cost aur labor time par adharit hai. Predicted value story depth aur originality ke premium multiplier se nikali gayi hai.")

                # Final Rewards
                st.divider()
                st.write(f"**Total Environment Reward:** {reward.value}")
                st.progress(reward.value)

if __name__ == "__main__":
    main()