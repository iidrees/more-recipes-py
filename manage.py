import os

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from main import app, db
# import worker

# app.config.from_object(os.environ["APP_SETTINGS"])


Migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__=='__main__':
    manager.run()