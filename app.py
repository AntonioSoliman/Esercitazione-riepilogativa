from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
import requests
from models import db, User

app = Flask (__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///utenti.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'


db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(id_user):
    return User.query.get(int(id_user))

@app.route('/home')
@login_required
def home():
   
    return render_template('home.html', username=current_user.username)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        if User.query.filter_by(username=username).first():
            return render_template('registrazione.html', error="Questo username è già in uso.")

        new_user = User(username=username, password=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('home'))
        except Exception as e:
            db.session.rollback()
            return render_template('registrazione.html', error=f"Errore durante la registrazione: {e}")
    return render_template('registrazione.html', error=None)


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))

        return render_template('login.html', error="Credenziali non valide.")
    return render_template('login.html', error=None)

if __name__ == "__main__":
    app.run(debug=True, port=5000)