#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import jsonify
from metaflask import app, auth

@app.route('/api/<page>', methods=['GET'])
def api(page):

	return jsonify()