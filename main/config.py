import os
from engines.nesus import start_nessus_scan
from engines.nmap_scanner import run_nmap_scan
from engines.nuceli_scanner import run_nuclei_scan
from engines.wpscan_scanner import run_wpscan


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = os.environ.get(
        'FLASK_DEBUG', 'False').lower() == 'true'  # Load from env

    DOJO_BASE_URL = os.environ.get('DOJO_BASE_URL')
    DOJO_AUTH_TOKEN = os.environ.get('DOJO_AUTH_TOKEN')

    CELERY_BROKER_URL = os.environ.get(
        'CELERY_BROKER_URL', 'redis://localhost:6379')
    CELERY_RESULT_BACKEND = os.environ.get(
        'CELERY_RESULT_BACKEND', 'redis://localhost:6379')

    IP_ENGINES = [
        run_nuclei_scan,
        start_nessus_scan,
        run_nmap_scan,
    ]

    DOMAIN_ENGINES = [
        run_nuclei_scan,
        start_nessus_scan,
        run_wpscan,
    ]


def load_config(app):
    app.config.from_object(Config)
