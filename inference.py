# inference.py

import os
from env.art_env import ArtEnv, Action
from utils.pricing import calculate_price

# sample input
data = {
    "material_cost": 100,
    "frame_cost": 50,
    "time_spent": 10,
    "size": "medium",
    "surface_type": "canvas",
    "detail_level": 7,
    "originality": 8,
    "story_score": 6
}

env = ArtEnv(data)

obs = env.reset()

predicted_price = calculate_price(data)

action = Action(
    predicted_price=predicted_price,
    description="Sample artwork"
)

obs, reward, done, info = env.step(action)

print("[START]")
print("Predicted:", predicted_price)
print("True:", env.true_price)
print("Reward:", reward.value)
print("[END]")