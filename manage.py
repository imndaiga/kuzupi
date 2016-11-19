#!/usr/bin/env python3
from flask_script import Manager, Shell
from app import create_app
import os

app = create_app(os.getenv('KUZUPI_CONFIG') or 'default')

manager = Manager(app)

def make_shell_context():
	from app import tools
	return dict(tools=tools)
manager.add_command('shell', Shell(make_context=make_shell_context))

if __name__ == '__main__':
	manager.run()