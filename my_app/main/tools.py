# coding: utf-8

import hashlib

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