#!/usr/bin/python

import os
import argparse
import json

from metaflask.models import db, User, Role

def create_db():
	db.create_all()

def drop_db():
	db.drop_all()

def main():
	parser = argparse.ArgumentParser(description='Manage this Flask application.')
	parser.add_argument('command', help='the name of the command you want to run')
	parser.add_argument('--seedfile', help='the file with data for seeding the database')
	args = parser.parse_args()

	if args.command == 'create_db':
		create_db()
		print "DB created!"

		
	elif args.command == 'delete_db':
		drop_db()
		print "DB deleted!"

	elif args.command == 'seed_db' and args.seedfile:
		with open(args.seedfile, 'r') as f:
			seed_data = json.loads(f.read())

		for role in seed_data.get("roles"):
			name = role.get("name")
			desc = role.get("description")
			db_role = Role(name,desc)
			db.session.add(db_role)

		for user in seed_data.get("users"):
			username=user.get("username")
			password=user.get("password")
			role = user.get("role")
			print username,password,role
			db_user = User(username,password,role)
			db.session.add(db_user)

		db.session.commit()
		print "\nUser Data added to database!"
	else:
		raise Exception('Invalid command')

if __name__ == '__main__':
	main()
