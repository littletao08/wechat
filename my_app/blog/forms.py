# coding: utf-8

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, \
     BooleanField, SubmitField, FileField, SelectField, ValidationError
from wtforms.validators import Required, Email, Length, EqualTo

from my_app.models import Account


class LoginForm(FlaskForm):
    """
    用户登录表单类, 具有服务器端验证的功能
    """
    email = StringField(u'邮箱', validators=[Required(), Email()])
    password = PasswordField(u'密码', validators=[Required()])
    remember_me = BooleanField(u'记住登录状态')
    submit = SubmitField(u'登录')


class RegisterForm(FlaskForm):
    """
    用户注册表单
    """
    email = StringField(u'邮箱', validators=[Required(), Email()])
    name = StringField(u'用户名', validators=[Required(), Length(1, 64)])
    password = PasswordField(u'密码', validators=[Required()])
    repassword = PasswordField(u'确认密码', validators=[Required(),
        EqualTo('password', message=u'密码前后不一致')])
    submit = SubmitField(u'注册')

    def validate_email(self, field):
        if Account.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮箱地址已存在')

    def validate_name(self, field):
        if Account.query.filter_by(name=field.data).first():
            raise ValidationError(u'用户名已存在')


class AddWechatForm(FlaskForm):
    """
    添加公众号表单
    """
    app_id = StringField(u'app_id', validators=[Required()])
    app_secret = StringField(u'app_secret', validators=[Required()])
    wechat_id = StringField(u'微信公众号', validators=[Required()])
    token = StringField(u'接入token', validators=[Required()])
    submit = SubmitField(u'添加')

class AddMediaForm(FlaskForm):
    """
    添加素材表单
    """
    media_file = FileField(u'选择素材')
    media_type = SelectField(u'选择素材类型',
        choices=[('image', u'图片'), ('voice', u'语音'), ('video', u'视频'),
        ('thumb', u'缩略图')])
    submit = SubmitField(u'提交')