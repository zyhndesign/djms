# coding:utf-8

from ..core import db, Deleted
from sqlalchemy_utils.models import Timestamp
from flask_security import UserMixin


class User(db.Model, Timestamp, UserMixin, Deleted):
    __tablename__ = "user"

    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    fullname = db.Column(db.String(32))  # 姓名
    tel = db.Column(db.String(20))  # 联系电话
    password = db.Column(db.String(128))
    active = db.Column(db.Boolean(), default=True)
    role = db.Column(db.String(16))


    @property
    def roles(self):
        return [FakeRole(self.role)]

    def __eq__(self, other):
        return self.email == other or self.email == getattr(other, "email", None)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.email)


class FakeRole(object):
    def __init__(self, name):
        self.name = name