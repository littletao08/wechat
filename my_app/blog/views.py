# coding: utf-8

from flask import request, Blueprint, render_template, redirect, flash, url_for
from flask_login import current_user, login_user

from my_app.blog.forms import LoginForm
from my_app.models import Account

blog = Blueprint('blog', __name__)


@blog.route('/')
def index():
    return render_template('blog/index.html')

@blog.route('/regist', methods=['GET', 'POST'])
def regist():
    pass

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

        login_user(user, form.remember_me.data)
        flash(u'你已成功登录', 'success')
        return redirect(request.args.get('next') or url_for('blog.index'))

    if form.errors:
        flash(form.errors, 'danger')
        
    return render_template('blog/login.html', form=form)

@blog.route('/add-wechat', methods=['GET', 'POST'])
def add_wechat():
    pass


