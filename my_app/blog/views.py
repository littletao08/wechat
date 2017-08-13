# coding: utf-8

from flask import request, Blueprint, render_template, redirect, flash, url_for
from flask_login import current_user, login_user, login_required, logout_user

from my_app.blog.forms import LoginForm, RegisterForm, AddWechatForm
from my_app.models import Account, Token
from my_app import db

import my_app.main.tools as tools

blog = Blueprint('blog', __name__)


@blog.route('/')
def index():
    """
    网站的主页视图, 显示已登录用户的绑定情况
    """
    wechat_list = []
    if current_user.is_authenticated:
        wechat_list  = Account.query.filter_by(email=current_user.email).first_or_404().tokens.all()
    return render_template('blog/index.html', wechat_len=len(wechat_list), wechat_list=wechat_list)

@blog.route('/register', methods=['GET', 'POST'])
def register():
    """
    注册视图

    """
    if current_user.is_authenticated:
        flash(u'您已登录!', 'info')
        return redirect(url_for('blog.index'))

    form = RegisterForm(request.form)

    if form.validate_on_submit():
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        existing_username = Account.query.filter_by(name=name).first()

        if existing_username:
            flash(
                u'用户名或电子邮箱已存在, 请重新输入!',
                'warning'
                )
            return render_template('blog/register.html', form=form)

        account = Account()
        account.name = name
        account.email = email
        account.password = password
        db.session.add(account)
        db.session.commit()
        flash(u'您已注册, 请登录', 'success')
        return redirect(url_for('blog.index'))

    if form.errors:
        flash(form.errors, 'danger')

    return render_template('blog/register.html', form=form)

@blog.route('/login', methods=['GET', 'POST'])
def login():
    """
    登录视图函数, 密码验证, 登录后跳转
    """
    if current_user.is_authenticated:
        flash(u'您已登录!', 'info')
        return redirect(url_for('blog.index'))

    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data
        account = Account.query.filter_by(email=email).first()

        if not (account and account.check_password(password)):
            flash(u'用户名或密码错误', 'warning')
            return redirect(url_for('blog.login'))

        login_user(account, form.remember_me.data)
        flash(u'你已成功登录', 'success')
        return redirect(request.args.get('next') or url_for('blog.index'))

    if form.errors:
        flash(form.errors, 'danger')
        
    return render_template('blog/login.html', form=form)

@blog.route('/logout')
@login_required
def logout():
    """
    登出视图
    """
    logout_user()
    return redirect(url_for('blog.index'))

@blog.route('/add-wechat', methods=['GET', 'POST'])
@login_required
def add_wechat():
    """
    添加微信公众号视图, 绑定微信公众号
    提供相应的公众号信息, 接入公众号
    """
    form = AddWechatForm(request.form)
    if form.validate_on_submit():
        app_id = form.app_id.data
        app_secret = form.app_secret.data
        wechat_id = form.wechat_id.data
        token = form.token.data

        t = Token.query.filter_by(app_id=app_id).first()
        if t:
            flash(u'您所添加的微信app_id已存在, 请添加其他公众号', 'warning')
            return redirect(url_for('blog.add_wechat'))

        email = current_user.email
        account = Account.query.filter_by(email=email).first()

        t = Token()
        t.app_id = app_id
        t.app_secret = app_secret
        t.wechat_id = wechat_id
        t.token = token
        t.account = account

        db.session.add(t)
        db.session.commit()

        flash(u'添加公众号成功!', 'success')
        return redirect(url_for('blog.index'))

    if form.errors:
        flash(form.errors, 'danger')

    return render_template('blog/add-wechat.html', form=form)

@blog.route('/get-token/<app_id>', methods=['GET', 'POST'])
@login_required
def get_token(app_id):
    """
    用于测试获取access_token的视图, 
    在正式完成后应该删除
    """
    app_id = app_id
    t = Token.query.filter_by(app_id=app_id).first()
    app_secret = t.app_secret
    return tools.get_token(app_id, app_secret)