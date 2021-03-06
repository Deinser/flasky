#!/usr/bin/env python
#-*- coding:utf-8 -*-
from app import create_app,db
from flask_script import Manager
from app.models import User,Role,Post,Follow
from flask_migrate import Migrate,MigrateCommand
import os

app=create_app(os.getenv('FLASK_CONFIG') or 'default')
manager=Manager(app)
migrate=Migrate(app,db)

@manager.shell
def make_shell_context():
	return dict(app=app,db=db,User=User,Role=Role,Post=Post,Follow=Follow)
manager.add_command('db',MigrateCommand)


@manager.command
def datainit():
	Role.insert_roles()
	User.follow_me()

@manager.command
def deploy():
	"""run development tasks"""
	from flask_migrate import upgrade
	from app.models import Role,User
	
	upgrade()  
	
	Role.insert_roles()
	
	User.follow_me()
	
	
if __name__=='__main__':
	manager.run()