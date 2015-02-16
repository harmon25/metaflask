#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: harmoN
# @Date:   2015-02-13 16:31:58
# @Last Modified by:   harmoN
# @Last Modified time: 2015-02-15 15:31:41
from flask import jsonify, request, url_for,session, render_template,g,flash,redirect
from metaflask import app, auth
from metaflask.models import db, User


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

@auth.error_handler
def auth_error():
    return "&lt;h1&gt;Access Denied&lt;/h1&gt;"


@app.route('/api/login', methods=['POST'])
def login_api():
		username = request.json.get('u')
		password = request.json.get('p')
		# try to authenticate with username/password
		user = User.query.filter_by(username=username).first()
		if not user or not user.verify_password(password):
			return redirect(url_for('login'))
		g.user = user
		session['logged_in'] = True
		flash('You were logged in')
		return redirect(url_for('index'))


@app.route('/api/logout', methods=['GET'])
def logout_api():
		session.pop('logged_in', None)
		flash('You were logged out')
		return redirect(url_for('login'))

@app.route('/api/users', methods=['POST'])
def new_user():
	username = request.json.get('username')
	password = request.json.get('password')
	if username is None or password is None:
		abort(400)
	if User.query.filter_by(username=username).first() is not None:
		abort(400)
	user = User(username=username)
	user.hash_password(password)
	db.session.add(user)
	db.session.commit()
	return (jsonify({'username': user.username}), 201,
    	{'Location': url_for('get_user', id=user.id, _external=True)})


@app.route('/api/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})

@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})