# coding: utf-8

"""微信接收消息模块

包含各类微信消息时间的模块, 并有解析消息函数, 每个消息类有保存方法
"""

import time
import xml.etree.ElementTree as ET

from .. import models


def parse_xml(data):
    """接收消息方法

    将接收到的微信消息/事件的xml字符串解析成相应的消息类

    Args:
        data: 微信服务器推送的的原始xml字符串消息

    Returns:
        返回相应的接收消息类
    """
    if len(data) == 0:
        return None
    xmlData = ET.fromstring(data)
    msg_type = xmlData.find('MsgType').text
    if msg_type == 'text':
        return TextMsg(xmlData)
    elif msg_type == 'image':
        return ImageMsg(xmlData)
    elif msg_type == 'voice':
        return VoiceMsg(xmlData)
    elif msg_type == 'video' or msg_type == 'shortvideo':
        return VideoMsg(xmlData)
    elif msg_type == 'location':
        return LocationMsg(xmlData)
    elif msg_type == 'link':
        return LinkMsg(xmlData)
    elif msg_type == 'event':
        event_type = xmlData.find('Event').text
        if event_type == 'LOCATION':
            return LocationEvent(xmlData)
        elif event_type == 'CLICK':
            return ClickEvent(xmlData)
        elif event_type == 'VIEW':
            return ViewEvent(xmlData)
        elif event_type == 'scan':
            return ScanEvent(xmlData)
        elif event_type == 'subscribe' or 'unsubscribe':
            if xmlData.find('Ticket') is not None:
                return ScanEvent(xmlData)
            else:
                return EventMsg(xmlData)


class Msg(object):
    """接收消息基类

    接收微信基类, 声明共有属性及共有方法

    Attributes:
        CreateTime (int): 消息创建事件戳
        FromUserName (str): 微信发送者的open_id字符串
        MsgId (int): 用于消息排重的整型数字字符串
        MsgType (str): 表明消息类型的字符串
        ToUserName (str): 开发者微信号(这里是公众号的原始id)
    """

    def __init__(self, xmlData):
        """接收消息类初始化

        初始化接收消息类, 保存共有属性

        Args:
            xmlData: 经过解析的微信消息
        """
        self.ToUserName = xmlData.find('ToUserName').text
        self.FromUserName = xmlData.find('FromUserName').text
        self.CreateTime = xmlData.find('CreateTime').text
        self.MsgType = xmlData.find('MsgType').text
        msg_id = xmlData.find('MsgId')
        self.MsgId = msg_id.text if msg_id is not None else ''

    def save(self):
        """保存消息方法

        保存消息, 返回一个消息模型, 在其他调用中再保存在数据库

        Returns:
            返回消息模型, 供具体消息类使用
        """
        msg = models.Msg()
        msg.to_username = self.ToUserName
        msg.from_username = self.FromUserName
        msg.create_time = self.CreateTime
        msg.msg_type = self.MsgType
        return msg


class TextMsg(Msg):
    """文本消息类

    文本消息, 比基类增加的content属性

    Attributes:
        Content (str): 文本类消息的内容
    """

    def __init__(self, xmlData):
        super(TextMsg, self).__init__(xmlData)
        self.Content = xmlData.find('Content').text

    def save(self):
        msg = super(TextMsg, self).save()
        msg.content = self.Content
        return msg


class ImageMsg(Msg):
    """图片消息

    图片消息增加了media_id属性及PicUrl

    Attributes:
        MediaId (str): 图片消息媒体id,
            可以用多媒体下载接口拉取数据
        PicUrl (str): 图片链接(由微信系统生成)
    """

    def __init__(self, xmlData):
        super(ImageMsg, self).__init__(xmlData)
        self.PicUrl = xmlData.find('PicUrl').text
        self.MediaId = xmlData.find('MediaId').text

    def save(self):
        msg = super(ImageMsg, self).save()
        media = models.Media()
        t = models.Token.query.filter_by(wechat_id=self.ToUserName).first()
        media.app = t
        media.locale_url = ''
        media.media_type = 'image'
        media.created_at = int(time.time())
        media.media_id = self.MediaId
        media.pic_url = self.PicUrl
        msg.media = media
        return msg


class VoiceMsg(Msg):
    """语音消息

    语音消息与图片消息类似, 也有media_id, 并表明了语音消息的格式,
        开通语音识别的公众号还会有语音识别结果

    Attributes:
        Format (str): 语音格式, 如amr, speex等
        MediaId (str): 语音消息媒体id
        Recognition (str): 语音识别结果
    """

    def __init__(self, xmlData):
        super(VoiceMsg, self).__init__(xmlData)
        self.MediaId = xmlData.find('MediaId').text
        self.Format = xmlData.find('Format').text
        recognition = xmlData.find('Recognition')
        self.Recognition = recognition.text if recognition is not None else ''

    def save(self):
        msg = super(VoiceMsg, self).save()
        media = models.Media()
        t = models.Token.query.filter_by(wechat_id=self.ToUserName).first()
        media.app = t
        media.locale_url = ''
        media.media_type = 'voice'
        media.created_at = int(time.time())
        media.media_id = self.MediaId
        media.voice_format = self.Format
        media.voice_recognition = self.Recognition
        msg.media = media
        return msg


class VideoMsg(Msg):
    """视频消息

    视频消息其实涵盖了视频消息和小视频消息, 对应的MsgType分别为
        video和shortvideo, 这两类的消息的结构一样

    Attributes:
        MediaId (str): 视频消息媒体id, 可以调用多媒体文件下载接口拉取数据
        ThumbMediaId (str): 视频消息缩略图媒体id
    """

    def __init__(self, xmlData):
        super(VideoMsg, self).__init__(xmlData)
        self.MediaId = xmlData.find('MediaId').text
        self.ThumbMediaId = xmlData.find('ThumbMediaId').text

    def save(self):
        msg = super(VideoMsg, self).save()
        media = models.Media()
        t = models.Token.query.filter_by(wechat_id=self.ToUserName).first()
        media.app = t
        media.locale_url = ''
        media.media_type = 'video'
        media.created_at = int(time.time())
        media.media_id = self.MediaId
        media.thumb_media_id = self.ThumbMediaId
        msg.media = media
        return msg


class LocationMsg(Msg):
    """地理位置消息

    地理位置消息, 与上报地理位置事件有区别,
        与平时好友之间发送的地理位置消息一样

    Attributes:
        Label (str): 地理位置信息
        Location_X (float): 地理位置维度
        Location_Y (float): 地理位置经度
        Scale (float): 地图缩放大小
    """

    def __init__(self, xmlData):
        super(LocationMsg, self).__init__(xmlData)
        self.Location_X = xmlData.find('Location_X').text
        self.Location_Y = xmlData.find('Location_Y').text
        self.Scale = xmlData.find('Scale').text
        self.Label = xmlData.find('Label').text

    def save(self):
        msg = super(LocationMsg, self).save()
        location = models.Location()
        location.location_x = float(self.Location_X)
        location.location_y = float(self.Location_Y)
        location.scale = float(self.Scale)
        location.label = self.Label
        msg.location = location
        return msg


class LinkMsg(Msg):
    """链接消息

    链接消息, 不太常用, 好友分享时会用到,
        可以通过收藏将链接消息发给公众号

    Attributes:
        Description (str): 消息描述
        Title (str): 消息标题
        Url (str): 消息链接
    """

    def __init__(self, xmlData):
        super(LinkMsg, self).__init__(xmlData)
        self.Title = xmlData.find('Title').text
        self.Description = xmlData.find('Description').text
        self.Url = xmlData.find('Url').text

    def save(self):
        msg = super(LinkMsg, self).save()
        media = models.Media()
        t = models.Token.query.filter_by(wechat_id=self.ToUserName).first()
        media.app = t
        media.locale_url = ''
        media.media_type = 'link'
        media.created_at = int(time.time())
        media.url = self.Url
        media.title = self.Title
        media.Description = self.Description
        media.tecent_url = self.Url
        msg.media = media
        return msg


class EventMsg(Msg):
    """事件消息基类

    事件消息基类, 同时也是subscribe与unsubscribe事件类,
        普通消息相比, 少了MsgId

    Attributes:
        CreateTime (int): 消息创建时间
        Event (str): 时间类型
        FromUserName (str): 发送方账号(OpenId)
        MsgType (str): 消息类型, event
        ToUserName (str): 开发者微信号
    """

    def __init__(self, xmlData):
        super(EventMsg, self).__init__(xmlData)
        self.Event = xmlData.find('Event').text

    def save(self):
        msg = super(EventMsg, self).save()
        e = models.Event()
        e.event_type = self.Event
        msg.event = e
        return msg


class ScanEvent(EventMsg):
    """扫描带参数二维码事件

    如果用户还未关注公众号，则用户可以关注公众号，关注后微信会将带场景值关注事件推送给开发者
        如果用户已经关注公众号，则微信会将带场景值扫描事件推送给开发者

    Attributes:
        EventKey (str): 事件Key值
        Ticket (str): 二维码的ticket
    """

    def __init__(self, xmlData):
        super(ScanEvent, self).__init__(xmlData)
        self.EventKey = xmlData.find('EventKey').text
        self.Ticket = xmlData.find('Ticket').text

    def save(self):
        msg = super(ScanEvent, self).save()
        e = msg.event
        e.event_key = self.EventKey
        e.ticket = self.Ticket
        return msg


class LocationEvent(EventMsg):
    """上报地理位置事件

    用户进入公众号时上报地理位置, 或者每5s上报一次

    Attributes:
        Latitude (float): 地理位置经度
        Longitude (float): 地理位置维度
        Precision (float): 地理位置精度
    """

    def __init__(self, xmlData):
        super(LocationEvent, self).__init__(xmlData)
        self.Latitude = xmlData.find('Latitude').text
        self.Longitude = xmlData.find('Longitude').text
        self.Precision = xmlData.find('Precision').text

    def save(self):
        msg = super(LocationEvent, self).save()
        e = msg.event
        e.latitude = self.Latitude
        e.longitude = self.Longitude
        e.precision = self.Precision
        return msg


class ClickEvent(EventMsg):
    """点击菜单拉取信息事件

    菜单点击后, 会推送相应的key详细, 以便公众号回复特定内容

    Attributes:
        EventKey (str): 事件key值
    """

    def __init__(self, xmlData):
        super(ClickEvent, self).__init__(xmlData)
        self.EventKey = xmlData.find('EventKey').text

    def save(self):
        msg = super(ClickEvent, self).save()
        e = msg.event
        e.event_key = self.EventKey
        return msg


class ViewEvent(EventMsg):
    """点击菜单跳转链接事件

    菜单点击后, 会跳转到对应的url

    Attributes:
        EventKey (str): 设置跳转的url
    """

    def __init__(self, xmlData):
        super(ViewEvent, self).__init__(xmlData)
        self.EventKey = xmlData.find('EventKey').text

    def save(self):
        msg = super(ViewEvent, self).save()
        e = msg.event
        e.event_key = self.EventKey
        return msg
