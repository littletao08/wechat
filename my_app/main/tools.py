# coding: utf-8

import hashlib
import urllib
import urllib2
import json
import time

from flask import current_app

from my_app.models import Token
from my_app import db


def check_signature(signature, timestamp, nonce, token):
    """微信接入校验函数

    根据微信公众号官方文档对signature进行校验

    Args:
        signature: 微信加密签名, 字符串, signature结合了开发者填写
            的token参数和请求中的timestamp参数、nonce参数
        timestamp: 微信服务器请求参数, 时间戳字符串
        nonce: 微信服务器请求参数, 随机数字符串
        token: 微信接入时填写的字符串

    Returns:
        返回校验结果
        bool
    """
    temp = [token, timestamp, nonce]
    temp.sort()
    temp = ''.join(temp)
    result = hashlib.sha1(temp).hexdigest()

    if result == signature:
        return True
    else:
        return False


def get_fresh_token(app_id, app_secret):
    """获取access_token

    根据app_id和app_secret直接从微信服务器获取access_token

    Args:
        app_id: 微信公众号的app_id, 字符串
        app_secret: 微信公众号的app_secret, 字符串

    Returns:
        返回包含即时access_token和有效时长的字典
        dict
    """
    data = {
        'grant_type': 'client_credential',
        'appid': app_id,
        'secret': app_secret
    }

    res = urllib2.urlopen(
        current_app.config['ACCESS_TOKEN_URL'], urllib.urlencode(data))
    result = json.loads(res.read())
    return result


def get_token(app_id):
    """本地获取access_token

    通过app_id在数据库中查找对应的access_token

    Args:
        app_id: 要获取access_token的app_id, 字符串

    Returns:
        返回可用的access_token值
        str
    """
    at = Token.query.filter_by(app_id=app_id).first()
    current_time = int(time.time())

    if at.access_token is None or current_time > int(at.expired_time):
        app_secret = at.app_secret
        result = get_fresh_token(app_id, app_secret)
        access_token = result['access_token']
        expires_in = result['expires_in']
        at.access_token = access_token
        at.expired_time = current_time + int(expires_in)
        db.session.commit()
        return access_token
    else:
        return at.access_token
