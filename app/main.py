from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user
import logging
from app.models import HistoryIp
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
    REQUEST_COUNT_MAIN.labels(method='GET', endpoint='/').inc()
    logging.info('Resolved index page!')
    
    return render_template('index.html')

@main.route('/metrics')
def metrics():
    logging.info("Metrics route only for debug!")
    return generate_latest(REGISTRY), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@main.route('/grafana')
@login_required
def grafana():
    logging.info("Grafana route only for debug!")
    return redirect('https://shodanscanning.azurewebsites.net/grafana')

@main.route("/search")
def search():
    logging.info("Resolved search page!")
    return render_template('search.html')

@main.route("/alert_service")
def alert_service():
    logging.info("Resolved alert_service page!")
    return render_template('alert_service.html')

@main.route("/team")
def about():
    logging.info("Resolved team page!")
    return render_template("team.html")

@main.route('/profile')
@login_required # per garantire l'accesso solo ad utenti registrati
def profile():
    logging.info("Resolved profile page!")
    if current_user.is_authenticated:
        historyIpUser = HistoryIp.query.filter_by(emailUser=current_user.email)
        return render_template('profile.html', name=current_user.name, historyIpUser=historyIpUser)
    else: 
        return render_template('profile.html', name=current_user.name)
