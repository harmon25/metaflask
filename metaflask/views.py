#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, g
from metaflask import app

@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')