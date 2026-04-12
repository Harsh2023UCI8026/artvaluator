# import streamlit as st
# import os
# import requests
# import json
# from env.art_env import ArtEnv, Action


# # API Key Fetching
# API_KEY = os.environ.get("GEMINI_API_KEY")

# def get_ai_refinement(text, complexity, originality):
#     """Gemini API call via REST to bypass SDK 404/403 errors"""
#     url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
#     headers = {'Content-Type': 'application/json'}
#     prompt = (f"As a professional curator, refine this art description: '{text}'. "
#               f"Complexity: {complexity}/10, Originality: {originality}/10. "
#               f"Make it emotionally resonant and exhibition-ready.")
    
#     payload = {"contents": [{"parts": [{"text": prompt}]}]}
#     try:
#         response = requests.post(url, headers=headers, json=payload)
#         return response.json()['candidates'][0]['content']['parts'][0]['text']
#     except:
#         return f"A deep, creative work reflecting {originality}/10 originality and intricate detail."

# def main():
#     st.set_page_config(page_title="ArtValuator | Hackathon Edition", layout="wide")
#     st.title("🎨 ArtValuator")
#     st.write("Professional Art Evaluation & Strategic Marketplace Insights")

#     uploaded_file = st.file_uploader("Upload Artwork Image", type=["jpg", "png", "jpeg"])

#     if uploaded_file:
#         st.image(uploaded_file, caption="Target Artwork", width=500)
        
#         st.subheader("📝 Manual Artwork Metrics")
#         col1, col2 = st.columns(2)
        
#         with col1:
#             mat_cost = st.number_input("Material Cost (₹)", min_value=0.0, value=300.0)
#             frame_cost = st.number_input("Framing Cost (₹)", min_value=0.0, value=150.0)
#             work_hours = st.slider("Hours Spent", 1, 300, 12)
        
#         with col2:
#             originality = st.slider("Originality Score", 1, 10, 8)
#             story_depth = st.slider("Story Narrative Score", 1, 10, 7)
#             complexity = st.slider("Detail Level", 1, 10, 5)

#         user_desc = st.text_area("Initial Description", "Describe the soul of your work...")

#         if st.button("🚀 Execute Full Analysis"):
#             if not API_KEY:
#                 st.error("Missing GEMINI_API_KEY in Secrets!")
#                 return

#             with st.spinner("AI analyzing the environment..."):
#                 # 1. Medium Task: AI Description
#                 refined_desc = get_ai_refinement(user_desc, complexity, originality)

#                 # 2. Hard Task: Valuation Logic
#                 env_data = {
#                     "mat": mat_cost, "frame": frame_cost, "time": work_hours,
#                     "orig": originality, "story": story_depth, "detail": complexity
#                 }
#                 env = ArtEnv(env_data)
#                 obs, reward, done, info = env.step(Action(predicted_price=0.0, description=refined_desc))

#                 st.success("Analysis Complete!")
#                 st.divider()

#                 # --- EASY TASK: Sales Strategy & Website Promotion ---
#                 st.subheader("📍 Easy Task: Sales Strategy")
#                 st.info(f"Task Reward Contribution: {reward.value * 0.2:.4f}")
#                 st.markdown(f"""
#                 **Primary Recommendation:**
#                 * **[Sell-Buy-Artworks (My Portfolio)](https://sell-buy-artworks.netlify.app/):** Is website ko maine (developer) khud banaya hai. Aap yahan apni art upload karne ke liye request bhej sakte hain. Yahan se potential buyers direct aapse connect kar sakte hain. Contact details site par maujood hain!
#                 * **Other Channels:** Instagram for reach, Etsy for international shipping.
#                 """)

#                 # --- MEDIUM TASK: AI Description ---
#                 st.subheader("📝 Medium Task: Refined Description")
#                 st.info(f"Task Reward Contribution: {reward.value * 0.3:.4f}")
#                 st.write(refined_desc)

#                 # --- HARD TASK: Pricing Logic ---
#                 st.subheader("💰 Hard Task: Financial Valuation")
#                 st.info(f"Task Reward Contribution: {reward.value * 0.5:.4f}")
#                 c1, c2 = st.columns(2)
#                 c1.metric("Predicted Market Value", f"₹{info['pred']}")
#                 c2.metric("Actual Mathematical Value", f"₹{info['act']}")
                
#                 st.write(f"**Justification:** {info['justification']}")
#                 st.write(f"**Price Variance:** ₹{abs(info['pred'] - info['act'])}")

#                 # Reward Summary
#                 st.divider()
#                 st.write(f"**Total Reward Score:** {reward.value}")
#                 st.progress(reward.value)

# if __name__ == "__main__":
#     main()
















import streamlit as st
import os
import requests
import json
import dotenv
from ..env.art_env import ArtEnv, Action

# API Key Security
API_KEY = os.environ.get("GEMINI_API_KEY")

def get_ai_refinement(text, complexity, originality):
    """Bypasses SDK issues using Direct REST API Call"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    headers = {'Content-Type': 'application/json'}
    prompt = (f"Act as a professional art historian. Refine this description: '{text}'. "
              f"Include complexity {complexity}/10 and originality {originality}/10 into a professional narrative.")
    
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        response = requests.post(url, headers=headers, json=payload)
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return f"A unique creation with {originality}/10 originality and deep narrative layers."

def main():
    st.set_page_config(page_title="ArtValuator Pro", layout="wide")
    st.title("🎨 ArtValuator")
    st.write("Hackathon Submission: AI Art Environment")

    uploaded_file = st.file_uploader("Upload Artwork", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        st.image(uploaded_file, caption="Target Artwork", width=500)
        
        st.subheader("📝 Professional Inputs")
        col1, col2 = st.columns(2)
        
        with col1:
            mat_cost = st.number_input("Material Cost (₹)", min_value=0.0, value=400.0)
            frame_cost = st.number_input("Framing Cost (₹)", min_value=0.0, value=200.0)
            work_hours = st.slider("Time Spent (Hours)", 1, 500, 15)
        
        with col2:
            originality = st.slider("Originality Score", 1, 10, 8)
            story_depth = st.slider("Story Narrative Score", 1, 10, 7)
            complexity = st.slider("Detail/Complexity", 1, 10, 5)

        user_desc = st.text_area("Initial Description", "Describe the inspiration...")

        if st.button("🚀 Analyze Masterpiece"):
            if not API_KEY:
                st.error("Missing GEMINI_API_KEY in Secrets!")
                return

            with st.spinner("AI analyzing the environment..."):
                # 1. Medium Task: AI Description
                refined_desc = get_ai_refinement(user_desc, complexity, originality)

                # 2. Hard Task: Env Pricing Logic
                env_data = {"mat": mat_cost, "frame": frame_cost, "time": work_hours, "orig": originality, "story": story_depth, "detail": complexity}
                env = ArtEnv(env_data)
                _, reward, _, info = env.step(Action(predicted_price=0.0, description=refined_desc))

                st.success("Analysis Complete!")
                st.divider()

                # --- EASY TASK: SALES STRATEGY ---
                st.subheader("📍 Easy Task: Strategy & Rewards")
                st.info(f"Task Reward: {reward.value * 0.2:.4f}")
                st.markdown(f"""
                * **Sell-Buy-Artworks (My Portfolio):** [Visit Site](https://sell-buy-artworks.netlify.app/)
                  **Personal Note:** Is website ko maine (developer) khud banaya hai. Aap yahan apni art upload karne ke liye request bhej sakte hain. Yahan se log aapki art direct khareed sakte hain. Contact info website par hai!
                * **Secondary Platforms:** Behance, Instagram Art, Etsy.
                """)

                # --- MEDIUM TASK: DESCRIPTION ---
                st.subheader("📝 Medium Task: Refined Description")
                st.info(f"Task Reward: {reward.value * 0.3:.4f}")
                st.write(refined_desc)

                # --- HARD TASK: PRICING ---
                st.subheader("💰 Hard Task: Pricing Analysis")
                st.info(f"Task Reward: {reward.value * 0.5:.4f}")
                c1, c2 = st.columns(2)
                c1.metric("Predicted Market Price", f"₹{info['pred']}")
                c2.metric("Actual Mathematical Price", f"₹{info['act']}")
                
                st.write(f"**Justification:** {info['justification']}")
                st.write(f"**Price Difference:** ₹{abs(info['pred'] - info['act'])}")

                # Final Progress
                st.divider()
                st.write(f"**Total Environment Reward Score:** {reward.value}")
                st.progress(reward.value)

if __name__ == "__main__":
    main()

















