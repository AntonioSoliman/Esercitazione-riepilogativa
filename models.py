from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id_user = db.Column(db.Integer, primary_key=True)  # ID univoco dell'utente
    username = db.Column(db.String(80), unique=True, nullable=False)  # Username univoco
    password = db.Column(db.String(200), nullable=False)  # Password hashata

    def get_id(self):
        return str(self.id_user)
