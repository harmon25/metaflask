#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, g, session, request, flash, redirect, url_for
from metaflask import app, auth
from metaflask.models import db, User

@app.route('/',methods=['GET'])
@auth.login_required
def index():
    return render_template('index.html')


@app.route('/logout', methods=['GET'])
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('login'))

@app.route('/login',methods=['GET','POST'])
def login():
	if request.method == 'POST':
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
	else:
		return render_template('login.html')
