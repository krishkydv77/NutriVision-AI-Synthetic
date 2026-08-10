# Step 1: Python 3.11 official light image use karein
FROM python:3.11-slim

# Work directory set karein
WORKDIR /app

# System dependencies install karein (Image processing ke liye)
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Requirements file copy aur install karein
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Baaki saare project folders aur files copy karein
COPY . .

# Static uploads folder ensure karein
RUN mkdir -p static/uploads

# FastAPI port expose karein
EXPOSE 8000

# Uvicorn server run karein
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]