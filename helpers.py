import datetime
import requests
import os
from dotenv import load_dotenv
from flask import request
import pandas as pd

try:
    load_dotenv('.env')
except:
    pass

# Values for caching
MINUTE = 60
HOUR = 60 * MINUTE
HALFDAY = 12 * HOUR
DAY = 2 * HALFDAY
APP_SECRET = os.getenv('APP_SECRET')


def api_request(slug):
    return requests.get(f"{os.getenv('API_BASE')}{slug}&token={os.getenv('API_TOKEN')}").json()


def get_datetime_now():
    now = datetime.datetime.now()
    return now


def get_datetime_old(days_ago):
    old = datetime.datetime.now() - datetime.timedelta(days_ago)
    return old


def get_cache_key():
    return request.url


def beautify_log(json, resample_rule, last_n_days=None):
    df = pd.DataFrame(json)
    if last_n_days:
        df = df[df['t'] >= get_datetime_old(last_n_days).timestamp()]
    index = [datetime.datetime.fromtimestamp(t) for t in df['t']]
    df['c'].index = index
    clean_df = df['c'].resample(resample_rule).mean().round(2)
    timestamp_list = [datetime.datetime.strftime(t, '%d %b, %y') for t in clean_df.index.to_list()]

    return {"t": timestamp_list, "p": clean_df.to_list()}
