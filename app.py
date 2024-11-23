import logging
import structlog

from flask import Flask, jsonify, request
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)

metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Aplicação Flask para demonstração', version='1.0.0')


logging.basicConfig(
    format="%(message)s",
    level=logging.INFO,
)

logger = structlog.get_logger()

@app.before_request
def log_request_info():
    logger.info("Request", method=request.method, path=request.path)

@app.after_request
def log_response_info(response):
    logger.info("Response", status=response.status_code)
    return response


@app.route('/')
def index():
    return jsonify({'message': 'Hello, World!'})

@app.route('/status')
def status():
    return jsonify({'status': 'UP'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
