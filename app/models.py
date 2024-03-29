from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


class User(UserMixin, db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(64), index=True, unique=True)
    password_hash = db.Column(db.Unicode(256))
    post_template = db.Column(db.Unicode(256))
    authorPage = db.Column(db.Text)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login.user_loader
    def load_user(uid):
        return User.query.get(int(uid))


class Post(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_title = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    create_timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=False)
    update_timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def get_post(id):
        return Post.query.filter(Post.id == id, Post.current.is_(True)).first()