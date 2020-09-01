import datetime
import requests
import os
from dotenv import load_dotenv

try:
    load_dotenv('.env')
except:
    pass

# Values for caching
MINUTE = 60
HOUR = 60 * MINUTE
HALFDAY = 12 * HOUR
DAY = 2 * HALFDAY


def api_request(slug):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Token {os.getenv('API_TOKEN')}"
    }
    return requests.get(os.getenv('API_BASE') + slug, headers=headers).json()


def get_today():
    now = datetime.datetime.now()
    return now.strftime('%Y-%m-%d')


def get_days_ago(days):
    now = datetime.datetime.now()
    old = now - datetime.timedelta(days)
    return old.strftime('%Y-%m-%d')
