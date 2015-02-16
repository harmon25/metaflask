#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.httpauth import HTTPBasicAuth


app = Flask(__name__)
app.config.from_object('metaflask.config')

app.url_map.strict_slashes = False

auth = HTTPBasicAuth()

import metaflask.userapi, metaflask.views
#import metaflask.msfapi 