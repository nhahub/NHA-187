# producer/Dockerfile
FROM python:3.9-slim

WORKDIR /app

# 1. Install System Dependencies (for building some python libs)
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# 2. Install PyTorch (CPU) - Matching the worker version for consistency
RUN pip install --no-cache-dir torch==2.2.2 torchvision==0.17.2 --index-url https://download.pytorch.org/whl/cpu

# 3. Install App dependencies
RUN pip install --no-cache-dir \
    streamlit \
    kafka-python \
    pandas \
    transformers \
    safetensors \
    "numpy<2.0.0" \
    scikit-learn \
    joblib

# Copy the app code
COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]