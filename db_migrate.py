# coding:utf-8

from flask import Flask
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from program.core import db
from program.model import *


app = Flask(__name__)

app.config.from_object("program.settings")

db.init_app(app)

manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
