from app import app, db
from flask import render_template, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, ContentForm
from app.models import User, Post
from flask_login import current_user, login_user, logout_user, login_required
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
        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.password.data)
        with open('templates/default_author_page.html') as f:
            new_user.post_template = f.read()
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/authors')
def authors():
    return render_template('base.html')


@app.route('/about')
def about():
    return render_template('base.html')


@app.route('/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()


# @app.route('edit/<username>', methods=['GET', 'POST'])
# @login_required
# def edit_author_page(username):
#   if username != current_user.username:
#        return redirect(url_for(home))
#    form = ContentForm()
#    if request.method == 'GET':
#        form.content.data = current_user.author_page
#    if form.validate_on_submit():

@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    form = ContentForm()
    post = User.load_user(current_user.id).post_template
    if form.validate_on_submit():
        new_post = Post(post_title=form.post_title.data, body=form.post.data, author=current_user.id)
        db.session.add(new_post)
        db.session.commit()
    return render_template('post.html', form=form, post=post)


@app.route('/imageuploader', methods=['GET', 'POST'])
def imageuploader():
    return redirect(url_for('home'))
