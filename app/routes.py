from app import app
from flask import render_template
from app.forms import LoginForm


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)


