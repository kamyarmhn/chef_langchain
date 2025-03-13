FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port
EXPOSE 8501

# Set environment variables
ENV PYTHONPATH=/app

# Run the admin panel
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"] 