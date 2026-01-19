FROM python:3.12-slim

# Install system dependencies for GIS and Matplotlib
RUN apt-get update && apt-get install -y \
    build-essential \
    libgdal-dev \
    libproj-dev \
    libspatialindex-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and assets
COPY . .

# Ensure the posters directory exists
RUN mkdir -p posters

# Expose Gradio port
EXPOSE 7860

# Run the app
CMD ["python", "app.py"]
