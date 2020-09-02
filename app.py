from flask import Flask, jsonify, request, render_template
from flask_caching import Cache
from helpers import api_request, get_datetime_old, get_datetime_now, get_cache_key, beautify_log, get_net_gain
from helpers import MINUTE, DAY
from database import Database

app = Flask(__name__, static_url_path='/static')
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
db = Database()


@app.route('/')
@cache.cached(timeout=MINUTE)
def index():
    log = db.get_log_for_portfolio(1)
    total_gain = 0
    for stock in log:
        current = get_stock_price(stock['ticker'])['c']
        total_gain += get_net_gain(current, stock['price'], stock['shares'])
    return render_template("index.html", data={
        "total_gain": total_gain
    })


@app.route('/api/stock/<string:ticker>', methods=['GET'])
def get_stock_price(ticker):
    result = api_request(f"/quote?symbol={ticker}")
    return result


@app.route('/api/stock/history/<string:ticker>', methods=['GET'])
def get_stock_details(ticker):
    json = get_stock_price_log(ticker)
    result = beautify_log(json, 'W', 100)
    return jsonify(result)


@cache.cached(timeout=DAY, key_prefix=get_cache_key)
def get_stock_price_log(ticker):
    """Get historical data and cache it for 24 hrs"""
    json = api_request(f"/stock/candle?symbol={ticker}&resolution=60&from={get_datetime_old(1).timestamp()}&to={get_datetime_now().timestamp()}")
    return json


if __name__ == '__main__':
    app.run(debug=True)
