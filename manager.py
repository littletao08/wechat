# coding: utf-8

import os

from flask_script import Manager, Shell

from my_app import create_app, db


app = create_app(os.environ.get('FLASK_CONFIG') or 'default')


def make_shell_context():
    return dict(app=app, db=db, AccessToken=AccessToken, Msg=Msg, User=User,
                Media=Media, Event=Event)


manager = Manager(app)
manager.add_command('shell', Shell(make_context=make_shell_context))

# @manager.command
# def test():
#     """运行单元测试"""
#     import unittest
#     tests = unittest.TestLoader().discover('tests')
#     unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
        manager.run()
