# coding: utf-8

import datetime as dt

from flask import Blueprint, request
from flask.views import MethodView

import requests

from tools import check_signature
from my_app.models import Token
from my_app import db
import receive
import reply

wechat = Blueprint('wechat', __name__)


class MainView(MethodView):
    """微信业务逻辑视图

    微信接入, 负责微信业务接入及消息处理的视图类

    Attributes:
        wechat: wechat蓝图
    """

    def get(self):
        """微信接入

        get请求处理, 验证消息是否为微信服务器发来, 接入微信公众号

        Returns:
            校验成功返回get参数echostr
        """
        app_id = request.args.get('app_id')
        signature = request.args.get('signature')
        timestamp = request.args.get('timestamp')
        nonce = request.args.get('nonce')
        echostr = request.args.get('echostr')

        t = Token.query.filter_by(app_id=app_id).first()

        if t is not None:
            token = t.token
            if check_signature(signature, timestamp, nonce, token):
                return echostr

        return u"校验失败"

    def post(self):
        """处理微信服务器推送过来的消息及事件

        处理微信服务器POST推送过来的各种消息及事件

        Returns:
            返回回复消息字符串, 微信公众平台文档中规定的精简版xml字符串消息
        """
        data = request.data
        print data
        msg = receive.parse_xml(data)
        try:
            m = msg.save()
            db.session.add(m)
            db.session.commit()
        except Exception as e:
            print str(e)

        reply_msg = reply.TextMsg()
        if isinstance(msg, receive.EventMsg):
            if msg.Event == 'subscribe':
                reply_msg.Content = u'欢迎订阅'
            elif msg.Event == 'CLICK':
                if msg.EventKey == 'news1':
                    item = reply.item()
                    item.Title = u'系统安装配置'
                    item.Description = u'系统安装与配置, windows, linux'
                    item.PicUrl = u'https://img3.doubanio.com/' \
                        'view/photo/l/public/p2497391244.webp'
                    item.Url = u'http://wangmiao.site/2017/07/29/' \
                        '%E7%B3%BB%E7%BB%9F%E5%AE%89%E8%A3%85%E5%8F%8A%E9%85%8D%E7%BD%AE/'

                    articles = [item]
                    reply_msg = reply.NewsMsg(articles)
                if msg.EventKey == 'news3':
                    articles = []
                    today = dt.date.today().toordinal()
                    for i in range(3):
                        params = {
                            'date': dt.date.fromordinal(today - i).isoformat()
                        }
                        res = requests.get('http://open.iciba.com/dsapi/',
                                           params=params)

                        print res.text
                        res = res.json()

                        item = reply.item()
                        item.Title = res['caption'] + res['dateline']
                        item.Description = res['content']
                        item.PicUrl = res['picture']
                        item.Url = 'http://news.iciba.com/views/dailysentence/daily.html#!/detail/title/' + res['dateline']
                        articles.append(item)
                    reply_msg = reply.NewsMsg(articles)
                if msg.EventKey == 'music':
                    music = reply.Music()
                    music.Title = u'Nothing on you'
                    music.Description = 'Beautiful girls all over the world' \
                        '\nI could be chasing but my time would be wasted'
                    music.MusicUrl = 'http://music.163.com/outchain/player?type=2&id=227707'
                    music.HQMusicUrl = 'http://music.163.com/outchain/player?type=2&id=227707'
                    reply_msg = reply.MusicMsg()
                    reply_msg.Music = music
            else:
                reply_msg.Content = u'这是一条' + msg.Event + u'事件'
        else:
            if msg.MsgType == 'image':
                reply_msg = reply.ImageMsg()
                image = reply.Image(msg.MediaId)
                reply_msg.Image = image
            elif msg.MsgType == 'voice':
                reply_msg = reply.VoiceMsg()
                voice = reply.Voice(msg.MediaId)
                reply_msg.Voice = voice
            elif msg.MsgType == 'video':
                reply_msg = reply.VideoMsg()
                video = reply.Video()
                video.MediaId = msg.MediaId
                video.Title = 'test'
                video.Description = 'just test'
                reply_msg.Video = video
            else:
                reply_msg.Content = u'这是一条' + msg.MsgType + u'消息'
        reply_msg.FromUserName = msg.ToUserName
        reply_msg.ToUserName = msg.FromUserName

        print reply_msg.send()
        try:
            return reply_msg.send()
        except Exception as e:
            print str(e)
        finally:
            m = reply_msg.save()
            db.session.add(m)
            db.session.commit()


main_view = MainView.as_view('main_view')
wechat.add_url_rule('/', view_func=main_view, methods=['GET', 'POST'])
