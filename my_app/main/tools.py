# coding: utf-8

import hashlib
import urllib
import urllib2
import json
import time
import os

from flask import current_app, make_response, send_file

import requests

from my_app.models import Token, Media
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


def upload_media(app_id, files, media_type):
    """上传临时素材函数

    Args:
        app_id (str): 微信公众号app_id
        files (file-like): 需要上传的类文件对象
        media_type (str): 临时素材的类型, image, voice, video, thumb

    Returns:
        response: Requests库返回的响应对象
    """
    token = get_token(app_id)
    data = {
        'access_token': token,
        'type': media_type
    }

    media_file = {
        'files': (files.filename, files.read())
    }
    url = current_app.config['ADD_MEDIA_URL']
    res = requests.post(url, files=media_file, data=data)
    r = res.json()

    media_id = ''
    if media_type == 'thumb':
        media_id = r['thumb_media_id']
    else:
        media_id = r['media_id']
    created_at = r['created_at']

    filename = media_id + os.path.splitext(files.filename)[1]
    save_path = os.path.join(
        current_app.config['UPLOAD_FOLDER'], filename
    ).replace('\\', '/')
    files.seek(0, 0)
    files.save(save_path)

    t = Token.query.filter_by(app_id=app_id).first()

    media = Media()
    media.media_id = media_id
    media.media_type = media_type
    media.created_at = int(created_at)
    media.locale_url = 'uploads/' + filename
    media.app = t

    db.session.add(media)
    db.session.commit()

    return res


def update_media(app_id):
    """更新所有未到期的临时素材

    通过app_id查找数据库中存在记录的素材, 下载本地不存在素材
    并在数据库中标记素材地址

    Args:
        app_id (str): 所需要更新素材的公众号app_id
    """
    access_token = get_token(app_id)
    t = Token.query.filter_by(app_id=app_id).first()
    medias = t.medias
    url = current_app.config['GET_MEDIA_URL']
    for m in medias:
        params = {
            'access_token': access_token,
            'media_id': m.media_id
        }
        now = int(time.time())
        if now - m.created_at < 259200:
            res = requests.get(url, params=params)
            filename = res.headers.get('Content-disposition').split('"')[1]
            save_path = os.path.join(
                current_app.config['UPLOAD_FOLDER'], filename
            )

            if not os.path.exists(save_path):
                with open(save_path, 'wb+') as f:
                    f.write(res.content)

            m.locale_url = 'uploads/' + filename
            db.session.add(m)

    db.session.commit()


def download_media(app_id, media_id):
    token = get_token(app_id)
    m = Media.query.filter_by(media_id=media_id).first()

    url = current_app.config['GET_MEDIA_URL']
    params = {
        'access_token': token,
        'media_id': media_id
    }

    res = requests.get(url, params=params)

    filename = res.headers.get('Content-disposition').split('"')[1]

    save_path = os.path.join(
        current_app.config['UPLOAD_FOLDER'], filename)

    if not os.path.exists(save_path):
        with open(save_path, 'wb+') as f:
            f.write(res.content)

    m.locale_url = 'uploads/' + filename

    db.session.add(m)
    db.session.commit()

    response = make_response(send_file(save_path))
    response.headers['Content-disposition'] = res.headers['Content-disposition']

    return response
