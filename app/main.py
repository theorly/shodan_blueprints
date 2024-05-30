from flask import Blueprint, render_template
import logging


#logging.basicConfig(filename='app.log', level=logging.INFO) 
logging.basicConfig(level=logging.INFO)       



main = Blueprint("main", __name__)

@main.route("/")
def home():
    logging.info('Richiesta ricevuta per la rotta index /')
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