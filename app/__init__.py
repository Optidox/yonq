from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_blogging import SQLAStorage, BloggingEngine

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
storage = SQLAStorage(db=db)
migrate = Migrate(app, db, render_as_batch=True)
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models
