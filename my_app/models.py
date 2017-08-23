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
    app_id = db.Column(db.String(255), unique=True)
    app_secret = db.Column(db.String(255))
    wechat_id = db.Column(db.String(255))
    token = db.Column(db.String(255))
    access_token = db.Column(db.String(255))
    expired_time = db.Column(db.Integer)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    account = db.relationship('Account',
                            backref=db.backref('tokens', lazy='dynamic'))

tags = db.Table('tags',
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                db.Column('user_id', db.Integer, db.ForeignKey('user.id')))


class Tag(db.Model):
    """用户标签类"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    count = db.Column(db.Integer)


class User(db.Model):
    """用户类"""
    id = db.Column(db.Integer, primary_key=True)
    app_id = db.Column(db.String(255))
    openid = db.Column(db.String(255))
    nickname = db.Column(db.String(255))
    sex = db.Column(db.String(255))
    language = db.Column(db.String(255))
    city = db.Column(db.String(255))
    province = db.Column(db.String(255))
    country = db.Column(db.String(255))
    headimageurl = db.Column(db.String(255))
    subscribe_time = db.Column(db.Integer)
    unionid = db.Column(db.String(255))
    remark = db.Column(db.String(255))
    tags = db.relationship('Tag', secondary=tags,
                           backref=db.backref('users', lazy='dynamic'))


class Msg(db.Model):
    """消息记录存储模型"""
    id = db.Column(db.Integer, primary_key=True)
    from_username = db.Column(db.String(255))
    to_username = db.Column(db.String(255))
    msg_type = db.Column(db.String(255))
    create_time = db.Column(db.Integer)
    content = db.Column(db.String(255))
    media_id = db.Column(db.Integer, db.ForeignKey('media.id'))
    media = db.relationship('Media',
                            backref=db.backref('msgs', lazy='dynamic'))
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    location = db.relationship('Location',
                               backref=db.backref('msgs', lazy='dynamic'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    event = db.relationship('Event',
                            backref=db.backref('msgs', lazy='dynamic'))


class Media(db.Model):
    """素材对象的数据模型"""
    id = db.Column(db.Integer, primary_key=True)
    media_id = db.Column(db.String(255))
    thumb_media_id = db.Column(db.String(255))
    media_type = db.Column(db.String(255))
    voice_format = db.Column(db.String(255))
    voice_recognition = db.Column(db.String(255))
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    music_url = db.Column(db.String(255))
    hq_music_url = db.Column(db.String(255))
    locale_url = db.Column(db.String(255))
    tecent_url = db.Column(db.String(255))
    expired_time = db.Column(db.Integer)
    app_id = db.Column(db.String(255), db.ForeignKey('token.app_id'))
    app = db.relationship('Token',
                          backref=db.backref('medias', lazy='dynamic'))


class Event(db.Model):
    """事件类型的东西"""
    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(255))
    event_key = db.Column(db.String(255))
    ticket = db.Column(db.String(255))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    precision = db.Column(db.Float)


class Location(db.Model):
    """存储地理位置"""
    id = db.Column(db.Integer, primary_key=True)
    location_x = db.Column(db.Float)
    location_y = db.Column(db.Float)
    scale = db.Column(db.Float)
    label = db.Column(db.String(255))
