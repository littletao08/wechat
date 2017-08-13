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
    """微信接入验证函数"""
    a = [token, timestamp, nonce]
    a.sort()
    a = ''.join(a)
    result = hashlib.sha1(a).hexdigest()

    if result == signature:
        return True
    else:
        return False

def get_fresh_token(app_id, app_secret):
    """直接从微信服务器获取access_token"""
    data = {
        'grant_type': 'client_credential',
        'appid': app_id,
        'secret': app_secret
    }

    res = urllib2.urlopen(
        current_app.config['ACCESS_TOKEN_URL'], urllib.urlencode(data))
    result = json.loads(res.read())
    return result

def get_token(app_id, app_secret):
    """尝试从本地获取token,如果过期则获取新的token并存入数据库"""
    at = Token.query.filter_by(app_id=app_id).first()
    current_time = int(time.time())

    if at.access_token is None or current_time > int(at.expired_time):
        result = get_fresh_token(app_id, app_secret)
        access_token = result['access_token']
        expires_in = result['expires_in']
        at.access_token = access_token
        at.expired_time = current_time + int(expires_in)
        db.session.commit()
        return access_token
    else:
        return at.access_token
