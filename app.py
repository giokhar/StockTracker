from flask import Flask, jsonify, request, render_template
from flask_caching import Cache
from helpers import api_request, get_datetime_old, get_datetime_now, get_cache_key, beautify_log
from helpers import MINUTE, DAY
from database import Database

app = Flask(__name__, static_url_path='/static')
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
db = Database()


@app.route('/api/stock/<string:ticker>', methods=['GET'])
def get_stock_price(ticker):
    result = api_request(f"/quote?symbol={ticker}")
    return result


@app.route('/')
# @cache.cached(timeout=MINUTE)
def index():
    log = db.get_log_for_portfolio(1)
    net_profit = 0
    investment = 0
    total = 0
    diff_today = 0

    for stock in log:
        ticker = get_stock_price(stock['ticker'])
        current = ticker['c']
        diff_today += current - ticker['o']
        investment += stock['price'] * stock['shares']
        total += current * stock['shares']
        net_profit += total - investment
    return render_template("index.html", data={
        "diff_today_positive": diff_today > 0,
        "diff_today": abs(diff_today),
        "investment": int(investment),
        "total": total,
        "net_profit": net_profit
    })


@app.route('/api/stock/history/<string:ticker>', methods=['GET'])
def get_stock_details(ticker):
    json = get_stock_price_log(ticker)
    result = beautify_log(json, 'W', 100)
    return jsonify(result)


@cache.cached(timeout=DAY, key_prefix=get_cache_key)
def get_stock_price_log(ticker):
    """Get historical data and cache it for 24 hrs"""
    json = api_request(
        f"/stock/candle?symbol={ticker}&resolution=60&from={get_datetime_old(1).timestamp()}&to={get_datetime_now().timestamp()}")
    return json


@app.template_filter()
def format_currency(value):
    return "{:,.2f}".format(value)


if __name__ == '__main__':
    app.run(debug=True)
