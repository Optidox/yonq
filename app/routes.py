from app import app, db
from flask import render_template, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm
from app.models import User
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
import requests
from html import unescape


@app.route('/')
def home():
    #emoji = unescape(requests.get('https://ranmoji.herokuapp.com/emojis/api/v.1.0/').json()['emoji'])
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            # insert invalid email/password handling
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, admin=False)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/blog')
def blog():
    return redirect(url_for('blogging.index'))


@app.route('/post', methods=['GET', 'POST'])
def post():
    return redirect(url_for('blogging.editor'))


@app.route('/authors')
def authors():
    return render_template('base.html')


@app.route('/about')
def about():
    return render_template('base.html')
