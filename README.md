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

## Installation
```bash
git clone git@github.com:old-joker/ParspackEngine.git
cd ParspackEngine
pip install -r requirements.py
gunicorn -w 4 -k gevent app:app -b 0.0.0.0:8080
docker run -d -p 6379:6379 redis
celery -A nuclei_tasks worker --loglevel=info -P eventlet
curl -X POST http://localhost:8080/run -H "Content-Type: application/json" -d '{"target": "http://example.com"}'
curl -X GET http://localhost:8080/status/<task_id>
```
