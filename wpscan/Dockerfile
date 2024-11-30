# Use the official Python image
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ruby build-essential libcurl4-openssl-dev libxml2 libxml2-dev libxslt1-dev ruby-dev libgmp-dev zlib1g-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN gem install wpscan
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

# Expose port 8093 for the FastAPI application
EXPOSE 8093

# Command to run the application
CMD ["uvicorn", "main:app","--workers", "4" ,"--host", "0.0.0.0", "--port", "8093"]
