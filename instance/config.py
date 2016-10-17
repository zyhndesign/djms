# coding:utf-8


SECRET_KEY = 'djms_secret'

SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://dbuser:dbpassword@192.168.2.104/djms"
# SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_ECHO = True

MAIL_DEFAULT_SENDER = "djms@qq.com"
MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = 465
# MAIL_USE_TLS = True
MAIL_USE_SSL = True
MAIL_USERNAME = "asset_hub@qq.com"
MAIL_PASSWORD = "asset111222"

SECURITY_PASSWORD_HASH = "sha256_crypt"
SECURITY_PASSWORD_SALT = "password_salt"
SECURITY_REMEMBER_SALT = "remember_salt"
SECURITY_RESET_SALT = "rest_salt"
