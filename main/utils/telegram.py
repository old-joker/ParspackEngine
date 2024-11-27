from datetime import datetime
import requests
from os import getenv

TELEGRAM_BOT_TOKEN = getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = getenv('TELEGRAM_CHAT_ID')

# SOCKS proxy configuration
PROXY_HOST = "germany.nonameperson.top"
PROXY_PORT = "51236"
PROXY_USER = "socks"
PROXY_PASS = "germanyy"
SOCKS_PROXY = f'socks5://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}'

def send_document_telegram(report_file_path):
    """Send report file to Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
    with open(report_file_path, 'rb') as report_file:
        files = {'document': report_file}
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        payload = {
            'chat_id': TELEGRAM_CHAT_ID,
            'caption': f"Here is the PsPack scan report at {timestamp}"
        }
        # Use the SOCKS proxy
        response = requests.post(url, data=payload, files=files, proxies={'http': SOCKS_PROXY, 'https': SOCKS_PROXY})
    return response.status_code == 200

def send_message_telegram(message):
    """Send a message to Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }
    # Use the SOCKS proxy
    response = requests.post(url, data=payload, proxies={'http': SOCKS_PROXY, 'https': SOCKS_PROXY})
    print(response.text)
    return response.status_code == 200
