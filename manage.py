#!/usr/bin/python

import os
import argparse
import json

from metaflask.models import db, User

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
	
		for user in seed_data:
			username=user.get("user")
			password=user.get("pass")
			role = user.get("role")
			db_user = User(username,password,role)
			db.session.add(db_user)

		db.session.commit()
		print "\nUser Data added to database!"
	else:
		raise Exception('Invalid command')

if __name__ == '__main__':
	main()
