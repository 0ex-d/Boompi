
import os
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from core import app, db


env = os.environ.get('APP_ENV')
app.config.from_object('config.%sConfig' % env.capitalize())

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()

