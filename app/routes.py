from flask import render_template, request
from app import app
from app.forms import LoginForm
from flask import flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app.models import User
#from app import posts  # Assuming posts is defined in app/__init__.py
from app import db
from urllib.parse import urlsplit

#VIEW FUNCTIONS
#main/home page
@app.route('/')
@app.route('/index')
@login_required  #protects login view function against anonymous users
def index():
    posts = {

    }
    return render_template("index.html", title='Home Page', posts=posts)

#login page and user authentication
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc !='':
            next_page = url_for('index')
        return redirect(next_page)
    

#logout page
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
  

#About page
@app.route('/about')
def about():
    return render_template('about.html', title='About')
