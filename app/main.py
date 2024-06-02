from flask import Blueprint, render_template
from flask_login import login_required, current_user
import logging
from app.models import HistoryIp


#logging.basicConfig(filename='app.log', level=logging.INFO) 
logging.basicConfig(level=logging.INFO)       



main = Blueprint("main", __name__)

@main.route("/")
def home():
    logging.info('Richiesta ricevuta per la rotta index /')
    if current_user.is_authenticated:
        historyIpUser = HistoryIp.query.filter_by(emailUser=current_user.email)
        return render_template('index.html', historyIpUser=historyIpUser)
    else:
        return render_template('index.html')

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

@main.route('/profile')
@login_required # per garantire l'accesso solo ad utenti registrati
def profile():
    return render_template('profile.html', name=current_user.name)
