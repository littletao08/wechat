# coding: utf-8

"""
回复消息的一些类
"""

import xml.etree.ElementTree as et
import time

from my_app import db
import my_app.models as models


class Msg(object):
    """回复消息基类"""

    def __init__(self, ToUserName=None,
                 FromUserName=None, CreateTime=None):
        self.ToUserName = ToUserName
        self.FromUserName = FromUserName
        self.CreateTime = str(int(time.time()))

    def send(self):
        try:
            result = et.tostring(to_element(self), encoding='utf-8')
        except Exception as e:
            print u'消息类转换错误', e
            result = 'success'
        return result

    def save(self):
        msg = models.Msg()
        msg.to_username = self.ToUserName
        msg.from_username = self.FromUserName
        msg.create_time = self.CreateTime
        return msg


class TextMsg(Msg):
    """文本消息"""

    def __init__(self, Content=None, **kwarg):
        super(TextMsg, self).__init__(**kwarg)
        self.Content = Content
        self.MsgType = 'text'

    def save(self):
        msg = super(TextMsg, self).save()
        msg.content = self.Content
        msg.msg_type = self.MsgType
        db.session.add(msg)
        db.session.commit()


class ImageMsg(Msg):
    """回复图片消息"""

    def __init__(self, Image=None, **kwarg):
        super(ImageMsg, self).__init__(**kwarg)
        self.Image = Image
        self.MsgType = 'image'

    def save(self):
        msg = super(ImageMsg, self).save()
        media_id = self.Image.MediaId
        media = models.Media.query.filter_by(media_id=media_id).first()
        msg.media = media
        db.session.add(msg)
        db.session.commit()


class Image(object):
    """图片类"""

    def __init__(self, MediaId=None):
        self.MediaId = MediaId


class VoiceMsg(Msg):
    """回复语音消息"""

    def __init__(self, Voice=None, **kwarg):
        super(VoiceMsg, self).__init__(**kwarg)
        self.Voice = Voice
        self.MsgType = 'Voice'

    def save(self):
        msg = super(VoiceMsg, self).save()
        media_id = self.Media.MediaId
        media = models.Media.query.filter_by(media_id=media_id).first()
        msg.media = media
        db.session.add(msg)
        db.session.commit()


class Voice(object):
    """语音类"""

    def __init__(self, MediaId=None):
        self.MediaId = MediaId


class VideoMsg(Msg):
    """回复视频消息"""

    def __init__(self, Video=None, **kwarg):
        super(VideoMsg, self).__init__(**kwarg)
        self.Video = Video
        self.MsgType = 'Video'

    def save(self):
        msg = super(VideoMsg, self).save()
        media_id = self.Video.MediaId
        media = models.Media.query.filter_by(media_id=media_id).first()
        msg.media = media
        db.session.add(msg)
        db.session.commit()


class Video(object):
    """视频类"""

    def __init__(self, MediaId=None, Title=None, Description=None):
        self.MediaId = MediaId
        self.Title = Title
        self.Description = Description


class MusicMsg(Msg):
    """回复音乐消息"""

    def __init__(self, Music=None, **kwarg):
        super(MusicMsg, self).__init__(**kwarg)
        self.Music = Music
        self.MsgType = 'music'

    def save(self):
        msg = super(MusicMsg, self).save()
        m = models.Media()
        m.media_id = self.Music.ThumbMediaId
        m.title = self.Music.Title
        m.description = self.Music.Description
        m.music_url = self.Music.MusicUrl
        m.hq_music_url = self.Music.HQMusicUrl
        msg.media = m
        db.session.add(msg)
        db.session.commit()


class Music(object):
    """歌曲类"""

    def __init__(self, Title=None, Description=None,
                 MusicUrl=None, HQMusicUrl=None, ThumbMediaId=None):
        self.Title = Title
        self.Description = Description
        self.MusicUrl = MusicUrl
        self.HQMusicUrl = HQMusicUrl
        self.ThumbMediaId = ThumbMediaId


class ArticleMsg(Msg):
    """图文消息类"""

    def __init__(self, Articles=None, **kwarg):
        super(ArticleMsg, self).__init__(**kwarg)
        self.ArticleCount = str(len(Articles))
        self.Articles = Articles
        self.MsgType = 'article'


class item(object):
    """图文消息条目"""

    def __init__(self, Title=None, Description=None, PicUrl=None, Url=None):
        self.Title = Title
        self.Description = Description
        self.PicUrl = PicUrl
        self.Url = Url


def to_element(obj, root='xml'):
    """将各消息类转化成ElementTree包下的Emlement"""
    e = et.Element(root)
    for k in obj.__dict__:
        if isinstance(getattr(obj, k), (str, unicode, int)):
            sub_e = et.Element(k)
            sub_e.text = getattr(obj, k)
            e.append(sub_e)
        elif isinstance(getattr(obj, k), type([])):
            e_l = et.Element(k)
            list_obj = getattr(obj, k)
            for i in list_obj:
                e_l.append(to_element(i, i.__class__.__name__))
            e.append(e_l)
        else:
            e.append(to_element(getattr(obj, k), k))
    return e
