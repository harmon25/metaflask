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
		g.user = user
		session['logged_in'] = True
		message = {"success": "true"}
		flash('You were logged in')
		return jsonify(message)

		
