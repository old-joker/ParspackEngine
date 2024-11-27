FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install WPScan
RUN apt-get update && apt-get install -y ruby
RUN apt-get install -y build-essential libcurl4-openssl-dev libxml2 libxml2-dev libxslt1-dev ruby-dev  libgmp-dev zlib1g-dev
RUN gem install wpscan
# Copy project files
COPY . .

# Expose the app on port 8093
EXPOSE 8093

# CMD ["python", "app.py"]
