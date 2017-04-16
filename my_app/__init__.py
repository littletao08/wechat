# coding: utf-8

"""
由于要从不同的配置类中动态的加载配置,
因此采用工厂函数的方式, 在运行时在初始化app
"""

import logging

from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import config


# 指定数据库
db = SQLAlchemy()
# 设置flask_login
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = u'请先登录.'
login_manager.login_message_category = 'warning'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])  # 加载配置

    # 初始化插件
    db.init_app(app)
    login_manager.init_app(app)

    # 注册各个蓝图模块到app
    from my_app.main.views import wechat
    from my_app.blog.views import blog
    app.register_blueprint(wechat, url_prefix='/wechat')
    app.register_blueprint(blog)

    # 初始化数据库
    with app.app_context():
        db.create_all()
        
    return app