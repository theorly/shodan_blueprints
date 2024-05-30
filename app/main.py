from flask import Blueprint, render_template
import logging
from prometheus_client import Counter, REGISTRY, generate_latest, CONTENT_TYPE_LATEST
from prometheus_flask_exporter import PrometheusMetrics


#logging.basicConfig(filename='app.log', level=logging.INFO) 
logging.basicConfig(level=logging.INFO)       

REQUEST_COUNT_MAIN = Counter('http_requests_total_main', 'Total HTTP Requests', ['method', 'endpoint'])


main = Blueprint("main", __name__)
metrics = PrometheusMetrics.for_app_factory()

@main.route("/")
@metrics.counter('home_requests', 'Number of requests to the main endpoint')
def home():
    logging.info('Richiesta ricevuta per la rotta index /')
    REQUEST_COUNT_MAIN.labels(method='GET', endpoint='/').inc()
    return render_template('index.html')

@main.route('/metrics')
def metrics():
    return generate_latest(REGISTRY), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@main.route("/search")
def search():
    logging.info('Richiesta ricevuta per la rotta search /')
    return render_template('search.html')

@main.route("/alert_service")
def alert_service():
    logging.info('Richiesta ricevuta per la rotta alert_service /')
    return render_template('alert_service.html')

@main.route("/team")
def about():
    logging.info('Richiesta ricevuta per la rotta team /')
    return render_template("team.html")