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
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码', validators=[Required()])
    remember_me = BooleanField('记住登录状态')
    submit = SubmitField('登录')


class RegisterForm(FlaskForm):
    """
    用户注册表单
    """
    email = StringField('邮箱', validators=[Required(), Email()])
    name = StringField('用户名', validators=[Required(), Length(1, 64)])
    password = PasswordField('密码', validators=[Required()])
    repassword = PasswordField('确认密码', validators=[Required(),
        EqualTo('password', message='密码前后不一致')])
    submit = SubmitField('注册')

    def validate_email(self, field):
        if Account.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱地址已存在')

    def validate_name(self, field):
        if Account.query.filter_by(name=field.data).first():
            raise ValidationError('用户名已存在')


class AddWechatForm(FlaskForm):
    """
    添加公众号表单
    """
    app_id = StringField('app_id', validators=[Required()])
    app_secret = StringField('app_secret', validators=[Required()])
    wechat_id = StringField('微信公众号', validators=[Required()])
    token = StringField('接入token', validators=[Required()])
    submit = SubmitField('添加')

class AddMediaForm(FlaskForm):
    """
    添加素材表单
    """
    media_file = FileField('选择素材')
    media_type = SelectField('选择素材类型',
        choices=[('image', '图片'), ('voice', '语音'), ('video', '视频'),
        ('thumb', '缩略图')])
    submit = SubmitField('提交')