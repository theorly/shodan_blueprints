from flask import Flask
import logging

from app import main
from app import search
from app import alert

logging.basicConfig(filename='app.log', level=logging.INFO)  


def create_app():
    app = Flask(__name__)
            
    logging.debug('Avvio dell\'applicazione Flask')

    app.register_blueprint(main.main)
    app.register_blueprint(search.host)
    app.register_blueprint(alert.alert)

    return app


