# coding: utf-8

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
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