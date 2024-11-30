# Patrowl Engine for ParsPack
## Overview
Patrowl Engine is a monitoring and management tool designed specifically for ParsPack infrastructure. It helps to automate and monitor various aspects of the hosting environment, ensuring smooth operation and quick detection of potential issues.
## Features
- **Automated Monitoring**: Continuously monitors the performance and status of the servers and services hosted on ParsPack.
- **Alerting System**: Sends notifications when predefined thresholds are reached (e.g., CPU usage, memory, bandwidth).
- **Log Aggregation**: Collects logs from multiple sources for centralized analysis.
- **Extensible Architecture**: Modular design to allow easy addition of new features and integrations.
## Requirements
- Python 3.8 or higher
- Flask (for API)
- Celery (for queue tasks)
- Redis (as a broker for Celery)
- FastAPI (for engines)
## Installation
# Docker
```bash
git clone git@github.com:old-joker/ParspackEngine.git --branch v2
cd ParspackEngine
docker compose build
docker compose up -d
```
# Test API Directly
```bash
curl -X POST "http://127.0.0.1:8091/scan" \
     -H "Content-Type: application/json" \
     -d '{
           "target": "scanme.nmap.org",
           "options": "-T4 -A"
         }'
```
