import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'screw-you-pattern-and-rellek'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BLOGGING_URL_PREFIX = "/blog"
    BLOGGING_DISQUS_SITENAME = "yonq"
    BLOGGING_SITEURL = "http://127.0.0.1:5000"
