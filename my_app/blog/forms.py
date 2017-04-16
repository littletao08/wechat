# coding: utf-8

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Email


class LoginForm(FlaskForm):
    """
    用户登录表单类, 具有服务器端验证的功能
    """
    email = StringField(u'邮箱', validators=[Required(), Email()])
    password = PasswordField(u'密码', validators=[Required()])
    remember_me = BooleanField(u'记住登录状态')
    submit = SubmitField(u'登录')