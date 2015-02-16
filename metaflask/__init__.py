#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
import config
from flask.ext.httpauth import HTTPBasicAuth


app = Flask(__name__)
app.config.from_object('config')

auth = HTTPBasicAuth()

import metaflask.userapi, metaflask.views, metaflask.msfapi 