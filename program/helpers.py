# coding:utf-8

import pkgutil
import importlib

from flask import Blueprint
from datetime import datetime, date
import uuid
from itsdangerous import json as _json


def register_blueprints(app, package_name, package_path):
    for _, name, _ in pkgutil.iter_modules(package_path):
        try:
            m = importlib.import_module("%s.%s" % (package_name, name))
            for item in dir(m):
                item = getattr(m, item)
                if isinstance(item, Blueprint):
                    app.register_blueprint(item)
        except Exception, e:
            print e


class JSONEncoder(_json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        if isinstance(obj, uuid.UUID):
            return str(obj)
        return super(JSONEncoder, self).default(obj)


