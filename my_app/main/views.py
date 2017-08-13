# coding: utf-8

from flask import Blueprint, request, current_app
from flask.views import MethodView

from my_app import db
from tools import check_signature
from my_app.models import Token
import receive
import reply


wechat = Blueprint('wechat', __name__)

class MainView(MethodView):
    """
    用于接入微信的视图类
    接入token是在绑定时候填写的
    接入地址是http://xxx.xx/wechat/?app_id=app_id
    """
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
                    return u"校验不通过"
            except Exception as e:
                return str(e), u'校验过程出错'

        return u"数据库比对失败"

    def post(self):
        """
        简单自动回复, 识别消息类型
        """
        data = request.data
        try:
            msg = receive.parse_xml(data)
            reply_msg = reply.TextMsg()
            reply_msg.FromUserName = msg.ToUserName
            reply_msg.ToUserName = msg.FromUserName
            if isinstance(msg, receive.EventMsg):
                if msg.Event == 'subscribe':
                    reply_msg.Content = u'欢迎订阅'
                else:
                    reply_msg.Content = u'这是一条' + msg.Event + u'事件'
            else:
                reply_msg.Content = u'这是一条' + msg.MsgType + u'消息'
            return reply_msg.send()
        except Exception as e:
            return 'success'
        finally:
            try:
                msg.save()
                reply_msg.save()
            except Exception as e:
                db.session.rollback()

main_view = MainView.as_view('main_view')
wechat.add_url_rule('/', view_func=main_view, methods=['GET', 'POST'])