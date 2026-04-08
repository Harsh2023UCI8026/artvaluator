---
title: ArtValuator
emoji: 🎨
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
---

# ArtValuator OpenEnv

## Motivation
ArtValuator is a real-world environment designed to help AI agents evaluate the fair market value of physical artwork. It models the complex relationship between material costs, time investment, and subjective artistic features.

## Action Space
The agent must provide:
- `predicted_price`: float (Estimated value in INR)
- `description`: string (Marketing/Curatorial text for the artwork)

## Observation Space
The environment returns:
- `predicted_price`: float
- `true_price`: float (Calculated baseline)
- `features`: Dictionary containing artwork metadata (size, material, complexity)

## Tasks & Difficulty
1. **Platform Recommendation** (Easy): Suggesting the right marketplace.
2. **Description Generation** (Medium): Creating engaging text based on visual features.
3. **Price Prediction** (Hard): Minimizing the variance between predicted and true market price.

## Setup Instructions
1. Build the image: `docker build -t artvaluator .`
2. Run the container: `docker run -p 7860:7860 artvaluator`

## Baseline Scores
- Easy Task: 0.95
- Medium Task: 0.82
- Hard Task: 0.70
