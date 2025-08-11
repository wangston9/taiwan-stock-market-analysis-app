FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy application files
COPY . .

# Expose port
EXPOSE 7860

# Health check
HEALTHCHECK CMD curl --fail http://localhost:7860/_stcore/health

# Run the Streamlit app
CMD ["streamlit", "run", "Dashboard_儀表板.py", "--server.port=7860", "--server.address=0.0.0.0"]