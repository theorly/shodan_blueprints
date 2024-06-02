from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import shodan
import logging

from app import main
from app import search
from app import alert


#logging.basicConfig(filename='app.log', level=logging.INFO)  
logging.basicConfig(level=logging.INFO)    

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
   
    #SHODAN_API_KEY = os.environ["SHODAN_API_KEY"]
    SHODAN_API_KEY = 'hJ4hcLWj7YK3PiIYKqhIaNf0Mw6uGNpQ'
    app.config['SECRET_KEY'] = SHODAN_API_KEY
    app.config['API_SHODAN'] = shodan.Shodan(SHODAN_API_KEY)
    #TODO mettere in var globali url e pass e #TODO fare un file config.py a parte
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://sambu:sambu@localhost/db_shodan'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://shodanpostgresql:I3moschettieri_@shodanpostgresqlserver.postgres.database.azure.com:5432/postgres?sslmode=require'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()
            
    logging.debug('Avvio dell\'applicazione Flask')

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    app.register_blueprint(main.main)
    app.register_blueprint(search.host)
    app.register_blueprint(alert.alert)

    return app


