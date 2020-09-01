from flask import Flask, jsonify, request
from flask_caching import Cache
from helpers import api_request, get_today, get_days_ago
from helpers import MINUTE, HALFDAY

app = Flask(__name__, static_url_path='/static')
cache = Cache(app, config={'CACHE_TYPE': 'simple'})


@app.route('/')
@cache.cached(timeout=MINUTE)
def index():
    return jsonify({"soso": "jemali"})


@app.route('/api/stock/<string:ticker>', methods=['GET'])
@cache.cached(timeout=MINUTE)
def get_stock_price(ticker):
    result = api_request(f"/daily/{ticker}/prices")
    return jsonify(result)


@app.route('/api/stock/history/<string:ticker>', methods=['GET'])
@cache.cached(timeout=HALFDAY)
def get_stock_historical_price(ticker):
    result = api_request(f"/daily/{ticker}/prices?startDate={get_days_ago(365)}&endDate={get_today()}&resampleFreq=daily")
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)