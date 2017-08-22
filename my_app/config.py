# coding: utf-8

import os

base_dir = os.path.join(os.path.dirname(__file__), 'static/data')


class Config(object):
    """关于配置参数的基类"""
    # 一个SECRET_KEY, 使一些需要加密的插件生效
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'my_secret_key'
    ACCESS_TOKEN_URL = 'https://api.weixin.qq.com/cgi-bin/token'
    ADD_TEMP_MEDIA_URL = 'https://api.weixin.qq.com/cgi-bin/media/upload'
    GET_TEMP_MEDIA_URL = "https://api.weixin.qq.com/cgi-bin/media/get"
    GET_TEMP_VIDEO_URL = "http://api.weixin.qq.com/cgi-bin/media/get"
    ADD_MEDIA_URL = \
        'https://api.weixin.qq.com/cgi-bin/material/add_material'
    ADD_MEDIA_NEWS_URL = \
        'https://api.weixin.qq.com/cgi-bin/material/add_news'
    # 文件上传配置
    UPLOAD_FOLDER = os.path.join(os.path.dirname(
        __file__), 'static/uploads').replace('\\', '/')
    ALLOWED_IMAGE = set(['png', 'jpg', 'jpeg', 'gif'])
    # 设置sqlalchemy一些参数
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # LOG_PATH = os.path.join(base_dir, 'log.log').replace('\\', '/')
    # # 配置email使正常发送
    # MAIL_SERVER = 'smtp.126.com'
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # MAIL_DEFAULT_SENDER = 'Wang Miao <tian7721@126.com>'


class DevelopmentConfig(Config):
    """开发环境下的配置类"""
    # 启用开发模式
    DEBUG = True
    # 指定开发环境的数据库地址
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or \
        'sqlite:///' + os.path.join(base_dir, 'data_dev.db').replace('\\', '/')


class TestingConfig(Config):
    """测试模式下的配置类"""
    # 启用测试模式
    TESTING = True
    # 指定测试环境的数据库地址
    # SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or \
    # 'sqlite:///' + os.path.join(base_dir, 'data_test.db').replace('\\', '/')


class ProductionConfig(Config):
    """生产环境下的配置类"""
    # 指定生产环境的数据库地址
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
        'sqlite:///' + os.path.join(base_dir, 'data.db').replace('\\', '/')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
