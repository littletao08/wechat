# coding: utf-8

from flask import Blueprint, render_template

blog = Blueprint('blog', __name__)


@blog.route('/')
def index():
    return render_template('blog/index.html')

@blog.route('/regist', methods=['GET', 'POST'])
def regist():
    pass

@blog.route('/login', methods=['GET', 'POST'])
def login():
    pass

@blog.route('/add-wechat', methods=['GET', 'POST'])
def add_wechat():
    pass


