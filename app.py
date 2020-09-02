from flask import Flask, jsonify, request, render_template
from flask_caching import Cache
from helpers import api_request, get_datetime_old, get_datetime_now, get_cache_key, beautify_log
from helpers import MINUTE, DAY
from database import Database

app = Flask(__name__, static_url_path='/static')
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
db = Database()


@app.route('/')
def index():
    log = db.get_log_for_portfolio(1)
    return render_template("index.html", data={
        "log": log
    })


@app.route('/api/stock/<string:symbol>', methods=['GET'])
@cache.cached(timeout=MINUTE)
def get_stock_price(symbol):
    result = api_request(f"/quote?symbol={symbol}")
    return result


@app.route('/api/stock/history/<string:symbol>', methods=['GET'])
def get_stock_details(symbol):
    json = get_stock_price_log(symbol)
    result = beautify_log(json, 'W', 100)
    return jsonify(result)


@cache.cached(timeout=DAY, key_prefix=get_cache_key)
def get_stock_price_log(symbol):
    """Get historical data and cache it for 24 hrs"""
    json = api_request(f"/stock/candle?symbol={symbol}&resolution=60&from={get_datetime_old(1).timestamp()}&to={get_datetime_now().timestamp()}")
    return json


if __name__ == '__main__':
    app.run(debug=True)
