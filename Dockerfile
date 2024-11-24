FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# Install Nuclei
RUN apt-get update && apt-get install -y wget unzip\
    && wget https://github.com/projectdiscovery/nuclei/releases/download/v2.9.8/nuclei_2.9.8_linux_amd64.zip \
    && unzip nuclei_2.9.8_linux_amd64.zip -d /usr/local/bin \
    && rm nuclei_2.9.8_linux_amd64.zip

# Preload templates (optional, useful for offline setups)
RUN mkdir -p /nuclei-templates \
    && nuclei -update-templates -ud /nuclei-templates

EXPOSE 8091
