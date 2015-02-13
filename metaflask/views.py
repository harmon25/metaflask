#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, g
from metaflask import app, auth

@app.route('/',methods=['GET'])
@auth.login_required
def index():
    return render_template('index.html')

@app.route('/login',methods=['GET'])
def login():
    return render_template('login.html')

