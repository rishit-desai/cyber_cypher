from flask import Flask, send_from_directory, request, Response
from flask_cors import CORS
import json
from predictPrice import predictPrice

# Create a Flask instance
app = Flask(__name__, static_folder='frontend/build', static_url_path='/')
CORS(app)

@app.route('/',defaults={'path': ''})
def serve(path):
    return send_from_directory(app.static_folder, 'index.html')


@app.errorhandler(404)
def page_not_found(e):
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/predict/<open>/<high>/<low>/<close>/<volume>/<adjclose>/<date>/<headline>', methods=['GET'])
def predict(open, high, low, close, volume, adjclose, date, headline):
    # Do something with the data
    data = {
        "open": open,
        "high": high,
        "low": low,
        "close": close,
        "volume": volume,
        "adjclose": adjclose,
        "date": date,
        "headline": headline
    }
    prediction = predictPrice(data=data)
    return_list = prediction.tolist()
    return Response(json.dumps({'prediction': return_list}),  mimetype='application/json')