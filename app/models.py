from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(64), index=True, unique=True)
    email = db.Column(db.Unicode(320), index=True, unique=True)
    password_hash = db.Column(db.Unicode(256))
    permissions = db.Column(db.String(16))

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login.user_loader
    def load_user(uid):
        return User.query.get(int(uid))
