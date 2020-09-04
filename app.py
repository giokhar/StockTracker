from flask import Flask, jsonify, request, render_template
from flask_caching import Cache
from helpers import api_request, get_datetime_old, get_datetime_now, get_cache_key, beautify_log
from helpers import MINUTE, DAY
from database import Database

app = Flask(__name__, static_url_path='/static')
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
db = Database()


@app.route('/')
# @cache.cached(timeout=MINUTE)
def index():
    p_id = request.args.get('p_id', 1)
    log = db.get_log_for_portfolio(p_id)
    portfolio = {
        "investment": 0,
        "current": 0,
        "net_profit": 0,
        "total_last_day": 0,
        "total_percent": 0,
    }
    diff = {
        "today": 0,
        "today_percent": 0,
        "today_positive": True
    }

    for stock in log:
        ticker = get_stock_price(stock['ticker'])
        if stock['is_buy']:
            portfolio['investment'] += stock['price'] * stock['shares']
            portfolio['current'] += ticker['c'] * stock['shares']
            portfolio['net_profit'] += portfolio['current'] - portfolio['investment']
            diff['today'] += (ticker['c'] - ticker['pc']) * stock['shares']
            portfolio['total_last_day'] += ticker['pc'] * stock['shares']
        else:
            portfolio['investment'] -= stock['price'] * stock['shares']
            portfolio['current'] -= ticker['c'] * stock['shares']
            portfolio['net_profit'] -= portfolio['current'] - portfolio['investment']
            diff['today'] -= (ticker['c'] - ticker['pc']) * stock['shares']
            portfolio['total_last_day'] -= ticker['pc'] * stock['shares']

    diff['today_positive'] = diff['today'] > 0
    diff['today'] = abs(diff['today'])
    diff['today_percent'] = abs(diff['today'] / portfolio['total_last_day']) * 100
    portfolio['investment'] = int(portfolio['investment'])
    portfolio['total_percent'] = (portfolio['current'] - portfolio['investment']) / portfolio['investment'] * 100

    return render_template("index.html", data={
        "stock_list": db.get_stocks_in_portfolio(p_id),
        "diff": diff,
        "portfolio": portfolio,
    })


@app.route('/api/stock/<string:ticker>', methods=['GET'])
def get_stock_price(ticker):
    result = api_request(f"/quote?symbol={ticker}")
    return result


@app.route('/api/stocks/portfolio/<int:p_id>', methods=['GET'])
def get_portfolio(p_id):
    result = db.get_stocks_in_portfolio(p_id)
    return jsonify(result)


@app.route('/api/stock/history/<string:ticker>', methods=['GET'])
def get_stock_details(ticker):
    json = get_stock_price_log(ticker)
    result = beautify_log(json, 'M', 365)
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
