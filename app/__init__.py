from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import shodan
import logging
import os
from prometheus_flask_exporter import PrometheusMetrics



#logging.basicConfig(filename='app.log', level=logging.INFO)  
logging.basicConfig(level=logging.INFO)    

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)


    #TODO da modificare per azure
    SHODAN_API_KEY = os.environ["SHODAN_API_KEY"]
    app.config['SECRET_KEY'] = SHODAN_API_KEY
    app.config['API_SHODAN'] = shodan.Shodan(SHODAN_API_KEY)
    #TODO mettere in var globali url e pass e #TODO fare un file config.py a parte
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["SQLALCHEMY_DATABASE_URI"]
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    import app.models as models 
    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return models.User.query.get(int(user_id))
    
    with app.app_context():
        db.create_all()

    # blueprint for auth routes in our app
    from app import auth    
   
    app.register_blueprint(auth.auth)

    from app import main
    from app import search
    from app import alert
    app.register_blueprint(main.main)
    app.register_blueprint(search.host)
    app.register_blueprint(alert.alert)


    metrics = PrometheusMetrics(app)
            
            
    logging.debug('Avvio dell\'applicazione Flask')

    return app


