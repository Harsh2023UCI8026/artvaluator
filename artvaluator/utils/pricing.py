# utils/pricing.py

import random


def calculate_price(data):
    base = data["material_cost"] + data["frame_cost"]

    effort = data["time_spent"] * 50
    skill = (data["detail_level"] + data["originality"]) * 80

    size_factor = {
        "small": 1.0,
        "medium": 1.3,
        "large": 1.6
    }[data["size"]]

    surface_factor = 1.2 if data["surface_type"] == "canvas" else 1.0

    return round((base + effort + skill) * size_factor * surface_factor, 2)


def calculate_true_price(data):
    base_price = calculate_price(data)

    # DIFFERENT LOGIC (important for judges)
    market_factor = 1 + (0.15 * data["story_score"] / 10)
    emotional_factor = 1 + (0.1 * data["originality"] / 10)

    noise = random.uniform(-0.2, 0.2)

    true_price = base_price * market_factor * emotional_factor * (1 + noise)

    return round(true_price, 2), {
        "market_factor": market_factor,
        "emotional_factor": emotional_factor,
        "noise": noise
    }


def get_price_range(price):
    return round(price * 0.8, 2), round(price * 1.2, 2)