# app/main.py

import os
import json

from utils.validation import validate_all
from utils.pricing import (
    calculate_price,
    get_price_range,
    generate_price_breakdown
)


def load_input(file_path):
    # reading input data from json file
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        return data
    except Exception as e:
        print("Error loading input file:", e)
        return None


def display_results(price, min_price, max_price, breakdown):
    # printing output in a clean way

    print("\n--- Price Estimation Result ---\n")

    print(f"Recommended Price: ₹{price}")
    print(f"Suggested Range: ₹{min_price} - ₹{max_price}\n")

    print("Breakdown:")
    print(f"- Base Cost: ₹{breakdown['base_cost']}")
    print(f"- Skill Contribution: ₹{breakdown['skill_score']}")
    print(f"- Size Factor: {breakdown['size_factor']}")
    print(f"- Surface Factor: {breakdown['surface_factor']}")

    print("\nNote:")
    print("This is an estimated fair price based on provided inputs.")
    print("You can adjust the price based on demand and audience.\n")


def main():
     

    # step 1: load input
    data = load_input("data/sample_input.json")

    if data is None:
        return

    # step 2: validate input
    is_valid, message = validate_all(data)

    if not is_valid:
        print("Validation Error:", message)
        return

    # step 3: calculate price
    price = calculate_price(data)

    # step 4: get price range
    min_price, max_price = get_price_range(price)

    # step 5: generate explanation
    breakdown = generate_price_breakdown(data)

    # step 6: display output
    display_results(price, min_price, max_price, breakdown)


if __name__ == "__main__":
    main()