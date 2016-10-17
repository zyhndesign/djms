# coding:utf-8

import os

DEBUG = True

basedir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

SECURITY_LOGIN_USER_TEMPLATE = "login.html"
SECURITY_POST_LOGIN_VIEW = "/djms/home"
SECURITY_POST_LOGOUT_VIEW = "/djms/login"
SECURITY_RESET_WITHIN = "3 days"
SECURITY_SEND_REGISTER_EMAIL = False
SECURITY_CONFIRMABLE = False
SECURITY_REGISTERABLE = False
SECURITY_CHANGEABLE = True
SECURITY_RECOVERABLE = True
SECURITY_POST_CHANGE_VIEW = "/djms/home"
SECURITY_POST_RESET_VIEW = "/djms/home"
SECURITY_UNAUTHORIZED_VIEW = "/djms/403"

SECURITY_MSG_EMAIL_NOT_PROVIDED = (u'邮箱不能为空', 'error')
SECURITY_MSG_PASSWORD_NOT_PROVIDED = (u'密码不能为空', 'error')
SECURITY_MSG_USER_DOES_NOT_EXIST = (u'用户不存在', 'error')
SECURITY_MSG_INVALID_PASSWORD = (u'无效的密码', 'error')

UPLOAD_FOLDER = os.path.join(basedir, "upload")
UPLOAD_URL = "http://192.168.2.104/djms/files"
