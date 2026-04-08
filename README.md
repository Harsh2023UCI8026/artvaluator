# ArtValuator

This project is inspired by a personal experience where I sold a painting at a very low price because I didn’t know its actual value.

The goal of this project is to help small and beginner artists estimate a fair price for their artwork.

The pricing is based on factors like:
- material cost
- time spent
- level of detail
- originality
- story behind the painting

This is not a fixed price system, but a structured way to estimate a fair value.

Features
1. Easy Task – Platform Recommendation

Based on the artwork description, the system suggests where the artist can sell their work.

Examples:

Instagram (for reach and audience engagement)
Etsy (for handmade and global buyers)
Fiverr / Upwork (for commission-based work)
ArtStation (for digital artists)

Additionally, artists can also use this platform:

https://sell-buy-artworks.netlify.app/

This platform allows artists to upload their artwork for free.
There is no commission, and artists can directly connect with the developer using the contact details provided on the website.

2. Medium Task – Artwork Description

The system helps improve how an artist presents their artwork.

Many artists create meaningful art but struggle to explain it properly to others.
This feature converts the basic input into a more structured and expressive description that:

Clearly explains what the artwork represents
Highlights the effort and detailing
Communicates the emotional value
Makes it easier for buyers to understand the piece
3. Hard Task – Price Estimation

The system calculates a recommended price using multiple factors:

Base cost (material + frame)
Effort (time spent)
Skill (detail level + originality)
Size multiplier
Surface type (canvas or paper)

It also calculates a true price (internal reference) using additional factors:

Emotional/story value
Market variation
Randomness to simulate real-world pricing uncertainty

This ensures that:

Predicted price and true price are not identical
The system reflects real market behavior
Reward System

The system evaluates how close the predicted price is to the internal true price.

Formula:

reward = 1 - (error / true_price)

Where:

error = difference between predicted and true price

This creates a continuous scoring system:

Better prediction → higher reward
Poor prediction → lower reward
Grading System

The project uses three levels of evaluation:

Task Level	What is Evaluated
Easy	Platform suggestions
Medium	Quality of description
Hard	Accuracy of pricing

Final Score = Average of all three tasks

System Flow

User uploads artwork
↓
Image is processed to extract features (size, detail level)
↓
User inputs additional details
↓
Price is calculated
↓
Description is improved
↓
Platform suggestions are generated
↓
Environment evaluates result
↓
Reward and final score are shown

Performance Optimizations
Image resizing for faster processing
Caching to avoid repeated computations
Lightweight logic for quick response
Fallback handling to avoid system failure
Setup Instructions
Install dependencies:

pip install -r requirements.txt

Create a .env file in the root directory:

GEMINI_API_KEY=your_api_key_here

Run the application:

streamlit run app/ui.py

Deployment

This project supports:

Docker deployment
Hugging Face Spaces
Why This Project Matters

This system is designed specifically for:

Small artists
Local creators
Beginners who are unsure about pricing

It helps them:

Understand the value of their work
Avoid underpricing
Present their artwork better
Find suitable platforms to sell
Future Improvements
Better image analysis using advanced models
Integration with real art marketplace data
Artist profile and reputation scoring
More accurate demand-based pricing