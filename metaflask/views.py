#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, g, session, request, flash, redirect, url_for, Response
from flask import send_file, make_response, abort, jsonify
from metaflask import app, auth
from metaflask.models import db, User

@app.route('/',methods=['GET'])
def index():
    return make_response(open('metaflask/templates/index.html').read())

@app.errorhandler(401)
def custom_401(error):
	message = {"success": False, "message": "Authentication Failed"}
	resp = jsonify(message)
	resp.status_code=401
	resp.headers['WWW-Authenticate'] = 'BasicCustom realm="metaflask"'
	return resp


@app.route('/logout', methods=['GET'])
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('login'))

def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d

@app.route('/login',methods=['POST'])
def login():
	username = request.json.get("username")
	password = request.json.get("password")
	# try to authenticate with username/password
	user = User.query.filter_by(username=username).first()
	if not user or not user.verify_password(password):
		abort(401)
		#raise InvalidAPIUsage(message, status_code=401) 
	else:
		user_auth = row2dict(user)
		g.user = username
		session['logged_in'] = True
		message = {"success": "true", "username": user_auth.get("username"), "role": user_auth.get("role")}
		flash('You were logged in')
		return jsonify(message)

		
