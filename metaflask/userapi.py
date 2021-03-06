#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: harmoN
# @Date:   2015-02-13 16:31:58
# @Last Modified by:   harmoN
# @Last Modified time: 2015-02-15 15:31:41
from flask import jsonify, request, url_for,session, render_template, g, flash,redirect, abort
from metaflask import app, jwt
from metaflask.models import db, User
from datetime import datetime
from flask_jwt import jwt_required, current_user

@jwt.authentication_handler
def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return False
    else:
        return user

@jwt.payload_handler
def make_payload(user):
    return {
        "user_id": user.id,
        "exp": str(datetime.utcnow() + app.config['JWT_EXPIRATION_DELTA'])
            }

@jwt.user_handler
def load_user(payload):
    if payload['user_id']:
        return User.query.filter_by(id=payload['user_id']).first()

@jwt.error_handler
def error_handler(error):
    message = {"success": False, "message": 'Authentication Failed'}
    resp = jsonify(message)
    resp.status_code=401
    resp.headers['WWW-Authenticate'] = 'BasicCustom realm="metaflask"'
    return resp

def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    return d


@app.route('/api/user', methods=['GET'])
@jwt_required()
def whoami():
	if current_user:
		user = current_user
		print user
		return jsonify({"username": user.username, "roles":str(user.roles)})
	else:
		 abort(400)



@app.route('/api/users', methods=['POST'])
def new_user():
	username = request.json.get('username')
	password = request.json.get('password')
	role = request.json.get('role')
	if username is None or password is None:
		abort(400)
	if User.query.filter_by(username=username).first() is not None:
		abort(400)
	user = User(username=username,role=role)
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

