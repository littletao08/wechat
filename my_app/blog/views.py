# coding: utf-8

from flask import request, Blueprint, render_template, redirect, flash, url_for
from flask_login import current_user, login_user

from my_app.blog.forms import LoginForm, RegisterForm
from my_app.models import Account
from my_app import db

blog = Blueprint('blog', __name__)


@blog.route('/')
def index():
    return render_template('blog/index.html')

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

@blog.route('/add-wechat', methods=['GET', 'POST'])
def add_wechat():
    pass


