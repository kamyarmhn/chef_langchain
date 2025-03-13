FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
COPY chat_interface/requirements.txt ./chat_interface/
COPY admin_panel/requirements.txt ./admin_panel/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir -r chat_interface/requirements.txt \
    && pip install --no-cache-dir -r admin_panel/requirements.txt

# Copy the rest of the application
COPY . .

# Expose ports
EXPOSE 8000
EXPOSE 8504

# Set environment variables
ENV PYTHONPATH=/app
ENV OLLAMA_HOST=http://ollama:11434

# Create a script to run both services
RUN echo '#!/bin/bash\n\
if [ "$SERVICE" = "chat" ]; then\n\
    chainlit run chat_interface/app.py --host 0.0.0.0\n\
elif [ "$SERVICE" = "admin" ]; then\n\
    streamlit run admin_panel/app.py --server.port 8504 --server.address 0.0.0.0\n\
fi' > /app/run.sh && chmod +x /app/run.sh

# Run the application
CMD ["/app/run.sh"] 