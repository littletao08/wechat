# coding: utf-8

"""
数据库模型
"""
from flask_login import UserMixin
from werkzeug import generate_password_hash, check_password_hash

from my_app import db, login_manager


class Account(UserMixin, db.Model):
    """微信公众平台用户类"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    password_hash = db.Column(db.String(255))

    @property
    def password(self):
        raise AttributeError('password is not readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
      return Account.query.get(int(user_id))


class Token(db.Model):
    """存放AccessToken的类"""
    id = db.Column(db.Integer, primary_key=True)
    app_id = db.Column(db.String(50), unique=True)
    app_secret = db.Column(db.String(256))
    wechat_id = db.Column(db.String(256))
    token = db.Column(db.String(256))
    access_token = db.Column(db.String(256))
    expired_time = db.Column(db.Integer)
    account_id = db.Column(db.String(50), db.ForeignKey('account.id'))
    account = db.relationship('Account',
                            backref=db.backref('tokens', lazy='dynamic'))