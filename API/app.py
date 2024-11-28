import logging
import structlog
from flask_cors import CORS
from manager import MediaManager
from flask import Flask, jsonify, request
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
manager = MediaManager()
CORS(app)
metrics = PrometheusMetrics(app, group_by='endpoint')
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

@app.get('/get-movies')
def get_movies():
    page = request.args.get('page', int())
    page = int(page) if type(page) is not int and page.isdigit() else int()
    return jsonify({'results': manager.get_medias(page)})

@app.get('/categories/<category>')
def get_movies_category(category):
    page = request.args.get('page', int())
    page = int(page) if type(page) is not int and page.isdigit() else int()
    return jsonify({'movie_data_by_categories': manager.get_medias_by_category(category, page)})

@app.get('/movies')
def get_movies_by_search():
    search = request.args.get('search')
    page = request.args.get('page', int())
    page = int(page) if type(page) is not int and page.isdigit() else int()
    if not search:
        return jsonify({'error': "Need to add a valid search term"})
    results = manager.get_medias_by_search(search, page)
    return jsonify({'results': manager.get_medias_by_search(search, page),
                    'length': len(results)})

@app.get('/genres')
def get_genres():
    return jsonify({'genres': manager.get_all_genres()})

@app.get('/best-movies')
def get_best_recommendations():
    page = request.args.get('page', int())
    page = int(page) if type(page) is not int and page.isdigit() else int()
    return jsonify({'results': manager.get_best_recommendations(page)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
