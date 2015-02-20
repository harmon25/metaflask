#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
import base64
from flask_jwt import JWT

app = Flask(__name__)
app.config.from_object('metaflask.config')
app.url_map.strict_slashes = False

jwt = JWT(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

import metaflask.userapi, metaflask.views
#import metaflask.msfapi 