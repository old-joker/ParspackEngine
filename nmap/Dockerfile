FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Nmap
RUN apt-get update && apt-get install -y nmap

# Copy project files
COPY . .

# Expose the app on port 8080
EXPOSE 8092

# CMD ["python", "app.py"]
