#!/usr/bin/env python

import os

from app import create_app, db
from app.models import User, Post, Category
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

application = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(application)
migrate = Migrate(application, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Post=Post, Category=Category)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def deploy():
    from app.models import User,Post, Category
    db.drop_all()
    db.create_all()

    # User.generate_fake(100)
    # Post.generate_fake(100)
    Category.insert_categories()


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == "__main__":
    manager.run()
