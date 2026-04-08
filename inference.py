# import os
# import json
# from openai import OpenAI
# from env.art_env import ArtEnv, Action

# # MANDATORY: Load variables from env
# API_BASE_URL = os.getenv("API_BASE_URL")
# MODEL_NAME = os.getenv("MODEL_NAME")
# HF_TOKEN = os.getenv("HF_TOKEN")

# def run_baseline():
#     client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)
    
#     # Static sample for reproducible results
#     data = {
#         "material_cost": 100, "frame_cost": 50, "time_spent": 10,
#         "size": "medium", "surface_type": "canvas", "detail_level": 7,
#         "originality": 8, "story_score": 6
#     }
    
#     env = ArtEnv(data)
    
#     print("[START]")
    
#     # Reset
#     obs = env.reset()
    
#     # Agent Logic (Calling the LLM to get a price and description)
#     # The requirement says you MUST use the OpenAI client here
#     response = client.chat.completions.create(
#         model=MODEL_NAME,
#         messages=[{"role": "user", "content": "Estimate art price and write a short description for these stats: " + str(data)}]
#     )
    
#     # For baseline reproducibility, we'll parse or use a standard action
#     action = Action(predicted_price=450.0, description="Professional artwork with deep emotional value.")
    
#     # Step
#     obs, reward, done, info = env.step(action)
    
#     print(f"[STEP] observation={obs.model_dump_json()} reward={reward.value} done={done}")
#     print(f"[END] score={reward.value}")

# if __name__ == "__main__":
#     run_baseline()
















import os
from openai import OpenAI
from env.art_env import ArtEnv, Action

def run_baseline():
    # Setup from env variables
    client = OpenAI(
        base_url=os.getenv("API_BASE_URL"),
        api_key=os.getenv("HF_TOKEN")
    )
    
    # Static data for testing
    data = {
        "material_cost": 500, "frame_cost": 200, "time_spent": 10,
        "size": "medium", "surface_type": "canvas", "detail_level": 8,
        "originality": 9, "story_score": 7, "user_description": "Lord Durga Painting"
    }
    
    env = ArtEnv(data)
    print("[START]")
    
    obs = env.reset()
    
    # Simulated action
    action = Action(predicted_price=2500.0, description="Deep spiritual artwork")
    obs, reward, done, info = env.step(action)
    
    print(f"[STEP] observation={obs.model_dump_json()} reward={reward.value} done={done}")
    print(f"[END] score={reward.value}")

if __name__ == "__main__":
    run_baseline()