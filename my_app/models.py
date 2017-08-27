# coding: utf-8

"""
数据库模型
"""
from flask_login import UserMixin
from werkzeug import generate_password_hash, check_password_hash

from my_app import db, login_manager


class Account(UserMixin, db.Model):
    """微信公众平台用户类

    开发平台用户, 用来绑定公众号

    Attributes:
        email (str): 用户邮箱
        id (int): 自增键
        name (str): 用户名
        password_hash (str): 用户密码哈希值
    """
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
    """公众号类

    开发平台用户绑定的公众号, 包含对应的公众号信息


    Attributes:
        access_token (str): 用来公众号权限的access_Ttoken
        account (str): 公众号账户外键
        account_id (str): 对应的账户id
        app_id (str): 公众号app_id
        app_secret (str): 公众号app_secret
        expired_time (int): 公众号access_token过期时间戳
        id (int): 自增键
        token (str): 公众号接入的token, 用于验证
        wechat_id (str): 公众号id
    """
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
    """用户标签类

    Attributes:
        count (str): 该标签下的用户数
        id (int): 自增键
        name (str): 标签名
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    count = db.Column(db.Integer)


class User(db.Model):
    """用户类

    用户类, 公众号订阅者的信息

    Attributes:
        app_id (str): 公众号的app_id
        city (str): 订阅用户所属城市
        country (str): 订阅用户所属国家
        headimageurl (str): 订阅用户头像链接
        id (int): 自增键id
        language (str): 订阅用户默认语言
        nickname (str): 订阅用户昵称
        openid (str): 订阅用户OpenId
        province (str): 订阅用户所属省份
        remark (str): 公众号对订阅用户的备注
        sex (str): 订阅用户性别
        subscribe_time (str): 用户订阅时间
        tags (str): 用户标签
        unionid (str): 只有在用户将公众号绑定到微信开放平台帐号后，才会出现该字段。
    """
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
    """消息记录存储模型

    消息记录模型, 存储公众号与订阅号之间的消息往来

    Attributes:
        content (str): text消息内容, 只有当消息类型为text时才不为空
        create_time (int): 消息创建时的时间戳
        event (str): 事件类型外键
        event_id (int): 事件类型外键id
        from_username (str): 消息发送者
        id (id): 自增键
        location (str): 地理位置外键
        location_id (id): 地理位置外键id
        media (str): 媒体素材外键
        media_id (int): 媒体素材外键id
        msg_type (str): 消息类型, text, image, voice, video,
            shortvideo, location, link, event
        to_username (str): 消息接收者
    """
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
    """素材数据模型

    素材数据模型, 订阅用户发送的多媒体素材, 公众用户上传的多媒体素材

    Attributes:
        app (str): 素材所属的公众号
        app_id (int): 素材所属公众号外键id
        description (str): 多媒体素材描述, video素材中描述
        expired_time (str): 临时素材过期时间
        hq_music_url (str): 高品质音乐链接
        id (str): 素材媒体数据库自增id
        locale_url (str): 媒体素材本地地址
        media_id (str): 素材媒体media_id
        media_type (str): 素材类型
        music_url (str): 回复音乐消息的地址
        tecent_url (str): 微信服务器上的媒体地址, 腾讯系外域名不可用
        thumb_media_id (str): 缩略图媒体id
        title (str): 标题
        voice_format (str): 语音消息格式
        voice_recognition (str): 语音识别结果
    """
    id = db.Column(db.Integer, primary_key=True)
    media_id = db.Column(db.String(255))
    thumb_media_id = db.Column(db.String(255))
    media_type = db.Column(db.String(255))
    created_at = db.Column(db.Integer)

    pic_url = db.Column(db.String(255))

    voice_format = db.Column(db.String(255))
    voice_recognition = db.Column(db.String(255))

    video_url = db.Column(db.String(255))

    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    url = db.Column(db.String(255))

    music_url = db.Column(db.String(255))
    hq_music_url = db.Column(db.String(255))

    article_count = db.Column(db.Integer)

    locale_url = db.Column(db.String(255))

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


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    pic_url = db.Column(db.String(255))
    url = db.Column(db.String(255))

    thumb_media_id = db.Column(db.String(255))
    author = db.Column(db.String(255))
    digest = db.Column(db.String(255))
    show_cover_pic = db.Column(db.Integer)
    content = db.Column(db.String(255))
    content_source_url = db.Column(db.String(255))

    article_id = db.Column(db.Integer, db.ForeignKey('media.id'))
    article = db.relationship('Media',
                              backref=db.backref('items', lazy='dynamic'))
