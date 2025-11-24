# processor/Dockerfile
FROM apache/spark:3.5.0

USER 0

# 1. Upgrade pip to ensure it handles versions correctly
RUN pip install --upgrade pip

# 2. Install libraries compatible with Python 3.8
# We pin 'filelock' because the newest version requires Python 3.9+
# We pin 'numpy<2' because NumPy 2.0 breaks many existing models
RUN pip install "filelock<3.13" "numpy<2.0.0"

# 3. Install PyTorch (CPU) - Version 2.2.2 is stable for Python 3.8
RUN pip install --no-cache-dir torch==2.2.2 torchvision==0.17.2 --index-url https://download.pytorch.org/whl/cpu

# 4. Install remaining libraries
RUN pip install --no-cache-dir \
    transformers \
    safetensors \
    pandas \
    scikit-learn \
    joblib \
    mysql-connector-python

USER 185