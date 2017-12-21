#!/usr/bin/env python
import os
from app import create_app, db
from app.models import Study, Role, Permission, Post
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from flaskext.markdown import Markdown
from flask import Flask, render_template, url_for
from flask_weasyprint import HTML, render_pdf



app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)
markdown = Markdown(app)


def make_shell_context():
    return dict(app=app, db=db, Study=Study, Role=Role, Permission=Permission, Post=Post)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
