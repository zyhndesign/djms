# coding:utf-8

from flask_mail import Mail
from flask_security import Security
from flask_sqlalchemy import SQLAlchemy, Model
from flask import g, abort, json
import sqlalchemy as sa
from sqlalchemy.orm.interfaces import SessionExtension
from sqlalchemy.orm import attributes
from dictalchemy.utils import asdict
from flask_security import SQLAlchemyUserDatastore
from decimal import getcontext


class Deleted(object):
    deleted = sa.Column(sa.Boolean, default=False, nullable=False)


class DeletedExtension(SessionExtension):
    def before_flush(self, session, flush_context, instances):
        for instance in session.deleted:
            if not isinstance(instance, Deleted):
                continue

            if not attributes.instance_state(instance).has_identity:
                continue

            # make it transient
            instance.deleted = True
            # re-add
            session.add(instance)


db = SQLAlchemy(session_options={
    "extension": [DeletedExtension()]
})
Model.asdict = asdict
mail = Mail()
security = Security()


class MySQLAlchemyUserDatastore(SQLAlchemyUserDatastore):
    def __init__(self, db, user_moel):
        SQLAlchemyUserDatastore.__init__(self, db, user_moel, None)

    def _prepare_create_user_args(self, **kwargs):
        kwargs.setdefault('active', True)
        return kwargs


class AppError(Exception):
    def __init__(self, code):
        self.code = code


def after_commit(f):
    callbacks = getattr(g, 'on_commit_callbacks', None)
    if callbacks is None:
        g.on_commit_callbacks = callbacks = []
    callbacks.append(f)
    return f


class BaseService(object):
    __model__ = None

    def save(self, model):
        db.session.add(model)
        db.session.flush()
        return model

    def get(self, model_id):
        if hasattr(self.__model__, 'deleted'):
            return self.__model__.query.filter(self.__model__.id == model_id, self.__model__.deleted == False).first()
        else:
            return self.__model__.query.get(model_id)

    def get_multi(self, model_ids):
        if hasattr(self.__model__, 'deleted'):
            return self.__model__.filter(self.__model__.id.in_(model_ids), self.__model__.deleted == False).all()
        else:
            return self.__model__.filter(self.__model__.id.in_(model_ids)).all()

    def get_all(self, order_by=None):
        if order_by is None:
            order_by = self.__model__.id.asc()
        if hasattr(self.__model__, 'deleted'):
            return self.__model__.query.filter(self.__model__.deleted == False).order_by(order_by).all()
        else:
            return self.__model__.query.order_by(order_by).all()

    def get_or_404(self, model_id):
        rv = self.get(model_id)
        if rv is None:
            abort(404)
        return rv

    def delete(self, model):
        db.session.delete(model)
        db.session.flush()

    def paginate_by(self, filters=[], order_by=None, offset=0, limit=10):
        if order_by is None:
            order_by = self.__model__.id.asc()

        if hasattr(self.__model__, 'deleted'):
            filters.append(self.__model__.deleted == False)

        data = []
        count = self.__model__.query.with_entities(db.func.count(self.__model__.id)).filter(*filters).scalar()
        if count:
            if offset is None and limit is None:
                data = self.__model__.query.filter(*filters).order_by(order_by)
            else:
                data = self.__model__.query.filter(*filters).order_by(order_by).offset(offset).limit(limit).all()

        return count, data




