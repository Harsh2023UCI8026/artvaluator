FROM python:3.10

# Step 1: Working directory set karein
WORKDIR /app

# Step 2: Sari files copy karein
COPY . /app

# Step 3: PYTHONPATH set karein taaki 'env.art_env' imports sahi chalein
ENV PYTHONPATH=/app

# Step 4: Streamlit specific settings (Hugging Face compatibility ke liye)
ENV STREAMLIT_SERVER_PORT=7860
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Step 5: Requirements install karein
RUN pip install --no-cache-dir -r requirements.txt

# Step 6: HF Space port expose karein
EXPOSE 7860

# Step 7: Final Command - Explicitly 0.0.0.0 aur port set karein
# Isse "Starting" wala error fix ho jayega
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]