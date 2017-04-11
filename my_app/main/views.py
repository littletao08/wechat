# coding: utf-8

from flask import Blueprint, request, current_app
from flask.views import MethodView

from my_app import db
from tools import check_signature


wechat = Blueprint('wechat', __name__)

class MainView(MethodView):
    """用于接入微信的视图类"""
    def get(self):
        signature = request.args.get('signature')
        timestamp = request.args.get('timestamp')
        nonce = request.args.get('nonce')
        echostr = request.args.get('echostr')
        token = current_app.config['WECHAT_TOKEN']

        try:
            if check_signature(signature, timestamp, nonce, token):
                return echostr
            else:
                return ""
        except Exception as e:
            return echostr

    def post(self):
       pass


main_view = MainView.as_view('main_view')
wechat.add_url_rule('/', view_func=main_view, methods=['GET', 'POST'])