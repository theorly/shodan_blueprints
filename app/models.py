from flask_login import UserMixin
from sqlalchemy import ForeignKeyConstraint
from . import db


class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(1000), nullable=False)

    def get_by_username(email):        
        db_user = User.query.filter(User.email == email).first()
        return db_user

    def __repr__(self):
        return f"<User {self.email}>"

class HistoryIp(db.Model):
    __tablename__ = 'historyIp'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True) # primary keys are required by SQLAlchemy
    ip = db.Column(db.String(100), nullable=False) #TODO migliorare il tipo di dato
    range = db.Column(db.Integer, nullable=False)
    emailUser = db.Column(db.String(100), nullable=False)

    __table_args__ = (        
        ForeignKeyConstraint([emailUser], [User.email], ondelete='NO ACTION'),        
    )
