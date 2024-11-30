# Use the official Python image
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget unzip \
    && wget https://github.com/projectdiscovery/nuclei/releases/download/v2.9.8/nuclei_2.9.8_linux_amd64.zip \
    && unzip nuclei_2.9.8_linux_amd64.zip -d /usr/local/bin \
    && rm nuclei_2.9.8_linux_amd64.zip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /nuclei-templates \
    && nuclei -update-templates -ud /nuclei-templates

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
EXPOSE 8092

# Command to run the application
CMD ["uvicorn", "main:app","--workers", "4" ,"--host", "0.0.0.0", "--port", "8092"]
