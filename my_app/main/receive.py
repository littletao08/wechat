# coding: utf-8

"""
接收到的微信消息类
"""

import xml.etree.ElementTree as ET
from my_app import db
import my_app.models as models


def parse_xml(data):
    """将xml字符串解析成消息类"""
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
    """接收到的微信消息的基类"""
    def __init__(self, xmlData):
        self.ToUserName = xmlData.find('ToUserName').text
        self.FromUserName = xmlData.find('FromUserName').text
        self.CreateTime = xmlData.find('CreateTime').text
        self.MsgType = xmlData.find('MsgType').text
        self.MsgId = xmlData.find('MsgId').text or ''

    def save(self):
        msg = models.Msg()
        msg.to_username = self.ToUserName
        msg.from_username = self.FromUserName
        msg.create_time = self.CreateTime
        msg.msg_type = self.MsgType
        return msg


class TextMsg(Msg):
    """文本消息类"""
    def __init__(self, xmlData):
        super(TextMsg, self).__init__(xmlData)
        self.Content = xmlData.find('Content').text

    def save(self):
        msg = super(TextMsg, self).save()
        msg.content = self.Content
        db.session.add(msg)
        db.session.commit()


class ImageMsg(Msg):
    """图片消息"""
    def __init__(self, xmlData):
        super(ImageMsg, self).__init__(xmlData)
        self.PicUrl = xmlData.find('PicUrl').text
        self.MediaId = xmlData.find('MediaId').text

    def save(self):
        msg = super(ImageMsg, self).save()
        media = models.Media()
        media.media_id = self.MediaId
        media.tecent_url = self.PicUrl
        msg.media = media
        db.session.add(msg)
        db.session.commit()


class VoiceMsg(Msg):
    """语音消息"""
    def __init__(self, xmlData):
        super(VoiceMsg, self).__init__(xmlData)
        self.MediaId = xmlData.find('MediaId').text
        self.Format = xmlData.find('Format').text
        self.Recognition = xmlData.find('Recognition').text or ''

    def save(self):
        msg = super(VoiceMsg, self).save()
        media = models.Media()
        media.media_id = self.MediaId
        media.voice_format = self.Format
        media.voice_recognition = self.Recognition
        msg.media = media
        db.session.add(msg)
        db.session.commit()


class VideoMsg(Msg):
    """视频消息"""
    def __init__(self, xmlData):
        super(VideoMsg, self).__init__(xmlData)
        self.MediaId = xmlData.find('MediaId').text
        self.ThumbMediaId = xmlData.find('ThumbMediaId').text

    def save(self):
        msg = super(VideoMsg, self).save()
        media = models.Media()
        media.media_id = self.MediaId
        media.thumb_media_id = self.ThumbMediaId
        msg.media = media
        db.session.add(msg)
        db.session.commit()


class LocationMsg(Msg):
    """地理位置消息"""
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
        db.session.add(msg)
        db.session.commit()


class LinkMsg(Msg):
    """链接消息"""
    def __init__(self, xmlData):
        super(LinkMsg, self).__init__(xmlData)
        self.Title = xmlData.find('Title').text
        self.Description = xmlData.find('Description').text
        self.Url = xmlData.find('Url').text

    def save(self):
        msg = super(LinkMsg, self).save()
        m = models.Media()
        m.media_id = self.Url
        m.title = self.Title
        m.Description = self.Description
        m.tecent_url = self.Url
        msg.media = m
        db.session.add(msg)
        db.session.commit()


class EventMsg(object):
    """事件消息基类(同时也是subscribe与unsubscribe事件类)"""
    def __init__(self, xmlData):
        self.ToUserName = xmlData.find('ToUserName').text
        self.FromUserName = xmlData.find('FromUserName').text
        self.CreateTime = xmlData.find('CreateTime').text
        self.MsgType = xmlData.find('MsgType').text
        self.Event = xmlData.find('Event').text

    def save(self):
        msg = models.Msg()
        msg.to_username = self.ToUserName
        msg.from_username = self.FromUserName
        msg.create_time = int(self.CreateTime)
        msg.msg_type = self.MsgType
        return msg


class ScanEvent(EventMsg):
    """扫描带参数二维码事件"""
    def __init__(self, xmlData):
        super(ScanEvent, self).__init__(xmlData)
        self.EventKey = xmlData.find('EventKey').text
        self.Ticket = xmlData.find('Ticket').text

    def save(self):
        msg = super(ScanEvent, self).save()
        e = models.Event()
        e.event_type = self.Event
        e.event_key = self.EventKey
        e.ticket = self.Ticket
        msg.event = e
        db.session.add(msg)
        db.session.commit()


class LocationEvent(EventMsg):
    """上报地理位置事件"""
    def __init__(self, xmlData):
        super(LocationEvent, self).__init__(xmlData)
        self.Latitude = xmlData.find('Latitude').text
        self.Longitude = xmlData.find('Longitude').text
        self.Precision = xmlData.find('Precision').text

    def save(self):
        msg = super(LocationEvent, self).save()
        e = models.Event()
        e.event_type = self.Event
        e.latitude = self.Latitude
        e.longitude = self.Longitude
        e.precision = self.Precision
        msg.event = e
        db.session.add(msg)
        db.session.commit()


class ClickEvent(EventMsg):
    """点击菜单拉取信息事件"""
    def __init__(self, xmlData):
        super(ClickEvent, self).__init__(xmlData)
        self.EventKey = xmlData.find('EventKey').text

    def save(self):
        msg = super(ClickEvent, self).save()
        e = models.Event()
        e.event_type = self.Event
        e.event_key = self.EventKey
        msg.event = e
        db.session.add(msg)
        db.session.commit()


class ViewEvent(EventMsg):
    """点击菜单跳转链接事件"""
    def __init__(self, xmlData):
        super(ViewEvent, self).__init__(xmlData)
        self.EventKey = xmlData.find('EventKey').text

    def function(self):
        msg = super(ViewEvent, self).save()
        e = models.Event()
        e.event_type = self.Event
        e.event_key = self.EventKey
        msg.event = e
        db.session.add(msg)
        db.session.commit()
