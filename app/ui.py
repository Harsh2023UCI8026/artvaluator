import streamlit as st
import os
import requests
import json
from env.art_env import ArtEnv, Action

# API Configuration
api_key = os.environ.get("GEMINI_API_KEY")

def get_gemini_response(prompt):
    """SDK ki jagah direct REST call taaki 404/403 errors fix ho jayein"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        raise Exception(f"API Error {response.status_code}: {response.text}")

def main():
    st.set_page_config(page_title="ArtValuator Pro", layout="wide")
    st.title("🎨 ArtValuator")
    st.write("Professional Evaluation & Marketplace Strategy Environment")

    uploaded_file = st.file_uploader("Artwork upload karein", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        st.image(uploaded_file, caption="Aapki Artwork", width=500)
        
        st.subheader("📊 Art Specifications (Manual Inputs)")
        col1, col2 = st.columns(2)
        
        with col1:
            mat_cost = st.number_input("Material Cost (₹)", min_value=0.0, value=200.0)
            frame_cost = st.number_input("Frame Cost (₹)", min_value=0.0, value=100.0)
            work_hours = st.slider("Kitne ghante kaam kiya? (Labor)", 1, 500, 10)
        
        with col2:
            originality = st.slider("Originality Score (1-10)", 1, 10, 7)
            story_depth = st.slider("Story Narrative Depth (1-10)", 1, 10, 6)
            complexity = st.slider("Detail Level (1-10)", 1, 10, 5)

        user_desc = st.text_area("Initial Description", value="Beautiful painting of Lord Durga on canvas")

        if st.button("🚀 Run Full AI Evaluation"):
            if not api_key:
                st.error("Secrets mein GEMINI_API_KEY nahi mili!")
                return

            try:
                with st.spinner("AI is analyzing..."):
                    # Task 2: Description Refinement
                    prompt = f"Refine this art description professionally: '{user_desc}'. Context: Detail {complexity}/10, Originality {originality}/10. Focus on the soul of the artwork."
                    refined_desc = get_gemini_response(prompt)

                    # Environment Logic
                    env_data = {
                        "mat": mat_cost, "frame": frame_cost, "time": work_hours,
                        "orig": originality, "story": story_depth, "detail": complexity
                    }
                    env = ArtEnv(env_data)
                    _, reward, _, info = env.step(Action(predicted_price=0.0, description=refined_desc))

                    st.success("Analysis Complete!")
                    st.divider()

                    # --- TASK 1: SALES STRATEGY (EASY) ---
                    st.subheader("📍 Easy Task: Sales Strategy")
                    st.info(f"Task Reward: {reward.value * 0.2:.4f}")
                    st.markdown(f"""
                    **Recommended Platforms:**
                    * **Sell-Buy-Artworks (Personal Website):** [Visit Site](https://sell-buy-artworks.netlify.app/)
                      Is website ko maine (Developer) khud banaya hai. Aap yahan apni artwork showcase karne ke liye mujhe request bhej sakte hain. Audience yahan se direct buy kar sakti hai. Contact details website par hain.
                    * **Instagram & Etsy:** Global reach aur prints bechne ke liye behtar hain.
                    """)

                    # --- TASK 2: AI DESCRIPTION (MEDIUM) ---
                    st.subheader("📝 Medium Task: Curated AI Description")
                    st.info(f"Task Reward: {reward.value * 0.3:.4f}")
                    st.write(refined_desc)

                    # --- TASK 3: PRICING (HARD) ---
                    st.subheader("💰 Hard Task: Financial Logic")
                    st.info(f"Task Reward: {reward.value * 0.5:.4f}")
                    c1, c2 = st.columns(2)
                    c1.metric("Predicted Market Value", f"₹{info['pred']}")
                    c2.metric("Actual Mathematical Value", f"₹{info['act']}")
                    
                    st.write(f"**Difference:** ₹{abs(info['pred'] - info['act'])}")
                    st.write("**Justification:** Actual value material+labor par adharit hai. Predicted value market demand aur story depth se influence hoti hai.")

                    # Rewards
                    st.divider()
                    st.write(f"**Final Environment Reward Score:** {reward.value}")
                    st.progress(reward.value)

            except Exception as e:
                st.error(f"Error: {e}")

if __name__ == "__main__":
    main()