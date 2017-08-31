# coding: utf-8

"""回复消息

回复消息模块, 包含各种类型的回复
"""

import xml.etree.ElementTree as et
import time

from .. import models as models


class Msg(object):
    """回复消息基类

    回复消息的基类, 包含其他各种具体回复消息类的共有属性

    Attributes:
        CreateTime (int): 消息创建时间戳
        FromUserName (str): 开发者微信号
        ToUserName (str): 公众号订阅者(OpenId)
    """

    def __init__(self, ToUserName=None,
                 FromUserName=None, CreateTime=None):
        self.ToUserName = ToUserName
        self.FromUserName = FromUserName
        self.CreateTime = str(int(time.time()))

    def send(self):
        """回复消息的发送

        发送方法, 将具体的回复消息类转换成xml字符串

        Returns:
            str: 返回符合微信公众平台要求的xml字符串
        """
        try:
            result = et.tostring(to_element(self), encoding='utf-8')
        except Exception as e:
            print u'消息类转换错误', e
            result = 'success'
        return result

    def save(self):
        """回复消息保存

        将回复消息保存在数据库中

        Returns:
            msg: 返回消息模型
        """
        msg = models.Msg()
        msg.to_username = self.ToUserName
        msg.from_username = self.FromUserName
        msg.create_time = self.CreateTime
        msg.msg_type = self.MsgType
        return msg


class TextMsg(Msg):
    """回复文本消息

    文本消息是基本的消息类型, 也是用的最多的类型

    Attributes:
        Content (str): 文本消息内容
        MsgType (str): 消息类型, text
    """

    def __init__(self, Content=None, **kwarg):
        super(TextMsg, self).__init__(**kwarg)
        self.Content = Content
        self.MsgType = 'text'

    def save(self):
        msg = super(TextMsg, self).save()
        msg.content = self.Content
        return msg


class ImageMsg(Msg):
    """回复图片消息

    图片消息中有图片类, 主要是为了转化成xml结构方便

    Attributes:
        Image (Image): 图片类
        MsgType (str): 消息类型, image
    """

    def __init__(self, Image=None, **kwarg):
        super(ImageMsg, self).__init__(**kwarg)
        self.Image = Image
        self.MsgType = 'image'

    def save(self):
        msg = super(ImageMsg, self).save()
        media = models.Media.query.filter_by(
            media_id=self.Image.MediaId).first()
        if media is None:
            media = models.Media()
            media.media_type = 'image'
            media.created_at = int(time.time())
            media.media_id = self.Image.MediaId
        msg.media = media
        return msg


class Image(object):
    """图片类

    图片类的创建, 在图片消息中使用

    Attributes:
        MediaId (str): 图片媒体id
    """

    def __init__(self, MediaId=None):
        self.MediaId = MediaId


class VoiceMsg(Msg):
    """回复语音消息

    回复语音消息与图片消息类似, 需要已给voice类

    Attributes:
        MsgType (str): 消息类型, voice
        Voice (Voice): Description
    """

    def __init__(self, Voice=None, **kwarg):
        super(VoiceMsg, self).__init__(**kwarg)
        self.Voice = Voice
        self.MsgType = 'voice'

    def save(self):
        msg = super(VoiceMsg, self).save()
        media = models.Media.query.filter_by(
            media_id=self.Voice.MediaId).first()
        if media is None:
            media = models.Media()
            media.media_type = 'voice'
            media.created_at = int(time.time())
            media.media_id = self.Voice.MediaId
        msg.media = media
        return msg


class Voice(object):
    """语音类

    语音类, 在语音消息中使用, 为了方便转换成xml结构

    Attributes:
        MediaId (str): 语音媒体id
    """

    def __init__(self, MediaId=None):
        self.MediaId = MediaId


class VideoMsg(Msg):
    """回复视频消息

    回复视频消息与语音消息类似, 需要一个单独的类video

    Attributes:
        MsgType (str): 消息类型, video
        Video (Video): Description
    """

    def __init__(self, Video=None, **kwarg):
        super(VideoMsg, self).__init__(**kwarg)
        self.Video = Video
        self.MsgType = 'video'

    def save(self):
        msg = super(VideoMsg, self).save()
        media = models.Media.query.filter_by(
            media_id=self.Voice.MediaId).first()
        if media is None:
            media = models.Media()
            media.media_type = 'video'
            media.created_at = int(time.time())
            media.media_id = self.Video.MediaId
        media.title = self.Video.Title
        media.description = self.Video.Description
        msg.media = media
        return msg


class Video(object):
    """视频类

    视频类, 在视频消息中使用, 与voice类类似, 多了Description和Title属性

    Attributes:
        Description (str): 视频描述, 非必须项
        MediaId (str): 视频媒体id, 必须公众号上传的
        Title (str): 视频标题, 非必须项
    """

    def __init__(self, MediaId=None, Title='', Description=''):
        self.MediaId = MediaId
        self.Title = Title
        self.Description = Description


class MusicMsg(Msg):
    """回复音乐消息

    回复音乐消息, 与视频类消息类似, 包含一个Music类

    Attributes:
        MsgType (str): 消息类型, music
        Music (Music): 音乐消息类
    """

    def __init__(self, Music=None, **kwarg):
        super(MusicMsg, self).__init__(**kwarg)
        self.Music = Music
        self.MsgType = 'music'

    def save(self):
        msg = super(MusicMsg, self).save()
        media = models.Media.query.filter_by(
            media_id=self.Music.ThumbMediaId).first()
        if media is None:
            media = models.Media()
            media.media_type = 'music'
            media.created_at = int(time.time())
            media.thumb_media_id = self.Music.ThumbMediaId
            media.title = self.Music.Title
            media.description = self.Music.Description
            media.music_url = self.Music.MusicUrl
            media.hq_music_url = self.Music.HQMusicUrl
        msg.media = media
        return msg


class Music(object):
    """音乐类

    音乐类, 包含音乐链接, 描述, 标题等信息

    Attributes:
        Description (str): 音乐消息描述, 非必须项
        HQMusicUrl (str): 高质量音乐链接, WiFi下优先使用, 非必须项
        MusicUrl (str): 音乐链接, 非必须项
        ThumbMediaId (str): 通过素材接口上传的缩略图的媒体id
        Title (str): 音乐消息标题, 非必须项
    """

    def __init__(self, Title='', Description='',
                 MusicUrl='', HQMusicUrl='', ThumbMediaId=''):
        self.Title = Title
        self.Description = Description
        self.MusicUrl = MusicUrl
        self.HQMusicUrl = HQMusicUrl
        self.ThumbMediaId = ThumbMediaId


class NewsMsg(Msg):
    """图文消息

    图文消息是最为复杂的回复消息类型, 多条图文组成的消息

    Attributes:
        ArticleCount (int): 图文消息个数, 限制为8条内
        Articles (list): 图文消息列表
        MsgType (str): 图文消息类型, 默认为news
    """

    def __init__(self, Articles=[], **kwarg):
        super(NewsMsg, self).__init__(**kwarg)
        self.ArticleCount = len(Articles)
        self.Articles = Articles
        self.MsgType = 'news'

    def save(self):
        msg = super(NewsMsg, self).save()

        m = models.Media()
        m.article_count = self.ArticleCount
        m.media_type = 'news'
        m.created_at = int(time.time())
        for i in self.Articles:
            item = models.Item()
            item.title = i.Title
            item.description = i.Description
            item.pic_url = i.PicUrl
            item.url = i.Url
            item.article = m

        msg.media = m
        return msg


class item(object):
    """图文消息条目

    每条图文消息为一个图片, 描述, 标题, 点击会跳转到详情页面
        默认第一条item显示为大图

    Attributes:
        Description (str): 图文消息描述
        PicUrl (str): 图片链接, 支持png, jpg, 大图360*200, 小图200*200
        Title (str): 图文消息标题
        Url (str): 点击图文消息跳转链接
    """

    def __init__(self, Title=None, Description=None, PicUrl=None, Url=None):
        self.Title = Title
        self.Description = Description
        self.PicUrl = PicUrl
        self.Url = Url


def to_element(obj, root='xml'):
    """消息格式转换函数

    将相应的回复消息类转换成Element对象

    Args:
        obj (msg): 具体的回复消息类
        root (str, optional): 可选的参数, 默认转换成的根元素为xml

    Returns:
        te.Element: 返回Element对象
    """
    e = et.Element(root)
    for k in obj.__dict__:
        if isinstance(getattr(obj, k), (str, unicode, int)):
            if getattr(obj, k) != '':
                sub_e = et.Element(k)
                sub_e.text = unicode(getattr(obj, k))
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
