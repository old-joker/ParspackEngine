# Use the official Python image
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    nmap \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Ensure the reports folder exists
RUN mkdir -p reports

# Expose port 8091 for the FastAPI application
EXPOSE 8091

# Command to run the application
CMD ["uvicorn", "main:app","--workers", "4" ,"--host", "0.0.0.0", "--port", "8091"]
