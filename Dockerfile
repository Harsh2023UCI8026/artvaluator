FROM python:3.10

WORKDIR /app
COPY . /app

# Set PYTHONPATH so imports like 'from env.art_env' work everywhere
ENV PYTHONPATH=/app
# Set Streamlit to run on the port required by Hugging Face
ENV STREAMLIT_SERVER_PORT=7860
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7860

CMD ["streamlit", "run", "app.py"]