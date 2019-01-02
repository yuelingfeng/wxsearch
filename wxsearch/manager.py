#coding=utf-8

from flask_script import Manager, Shell
from wxsearch import app,db,Users,dbmanage
from flask_migrate import Migrate, MigrateCommand

try:
    manage = Manager(app)

    migrate = Migrate(app, db)
    manage.add_command('model', MigrateCommand)

    manage.add_command('wxsearch', dbmanage)
except Exception as e:
    print(e)

def make_shell_context():
    return dict(app=app, db=db)
try:
    manage.add_command("shell", Shell(make_context=make_shell_context))
except Exception as e:
    print(e)

if __name__ == '__main__':
    manage.run()