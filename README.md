# 微信公众号管理系统

---------

本系统旨在打造一个完善的公众号管理系统, 实现一个账号管理多个公众号, 并使聊天记录, 用户信息等都记录在自己的服务器上, 为以后各种数据分析提供方便. 总体来说, 会有以下功能:

> * 多公众号绑定
> * 被动消息回复
> * 主动消息发送
> * 素材上传与存储
> * 消息记录存储与分析
> * 用户管理与分析

## 一. 部署及接入

尝试过在BAE和pythonanywhere上接入, 由于BAE上的mysql数据库速度非常慢, 现在在pythonanywhere上进行接入测试, 并且pw上还可以打开console, 对于开发来说非常方便

### BAE上部署

留空, 需要在BAE上接入请自行摸索, 流程是相似的

### pythonanywhere上部署

- 首先, 在[pythonanywhere](https://www.pythonanywhere.com)上注册账号

- 创建你的webapp, 在Working directory下运行git命令, 将github上的项目clone到pythonanywhere上

  ```shell
  git clone "https://github.com/oaim/wechat.git" wechat
  ```

- 配置运行环境, python2.7, 其他依赖环境可以通过根目录下requirement.txt文件安装

- 在pythonanywhere上创建mysql数据库

- 编辑WSGI configuration file, 添加相应的环境变量和配置程序入口:

  ```python
  import sys
  import os

  os.environ['FLASK_CONFIG'] = 'production'
  os.environ['DATABASE_URI'] = 'mysql+mysqldb://username:password@username.mysql.pythonanywhere-services.com/username$dbname'

  path = '/home/username/wechat'
  if path not in sys.path:
      sys.path.append(path)

  from manager import app as application
  ```

现在应该可以应该可以运行了

## 二. 完成进度说明

- [x] 系统账号注册与公众号绑定 
- [x] 多公众号接入
- [x] 接收消息解析
- [x] 被动回复消息
- [ ] 素材管理
- [ ] 主动回复消息
- [ ] 消息存储
- [ ] 网页前端渲染





## 三. 接收消息

## 四. 被动回复消息

## 五. 主动回复消息

## 六. 素材管理

## 七. 消息存储