# coding: utf-8

from flask import Blueprint, request, current_app
from flask.views import MethodView

from my_app import db
from tools import check_signature
from my_app.models import Token


wechat = Blueprint('wechat', __name__)

class MainView(MethodView):
    """用于接入微信的视图类"""
    def get(self):
        app_id = request.args.get('app_id')
        signature = request.args.get('signature')
        timestamp = request.args.get('timestamp')
        nonce = request.args.get('nonce')
        echostr = request.args.get('echostr')

        t = Token.query.filter_by(app_id=app_id).first()

        if t is not None:
            token = t.token

            try:
                if check_signature(signature, timestamp, nonce, token):
                    return echostr
                else:
                    print u'错误'
                    return ""
            except Exception as e:
                return echostr

        return ""

    def post(self):
       pass


main_view = MainView.as_view('main_view')
wechat.add_url_rule('/', view_func=main_view, methods=['GET', 'POST'])