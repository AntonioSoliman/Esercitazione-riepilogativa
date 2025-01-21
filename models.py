from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy()

class User(UserMixin, db.Model):
    id_user = db.Column(db.Integer, primary_key=True)  # ID univoco dell'utente
    username = db.Column(db.String(80), unique=True, nullable=False)  # Username univoco
    password = db.Column(db.String(200), nullable=False)  # Password hashata
   

    def __repr__(self):
        return f"<User(id={self.id_user}, username='{self.username}')>"