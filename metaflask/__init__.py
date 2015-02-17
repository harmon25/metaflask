#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.login import LoginManager


app = Flask(__name__)
app.config.from_object('metaflask.config')

app.url_map.strict_slashes = False

login_manager = LoginManager()

login_manager.init_app(app)


@login_manager.request_loader
def load_user_from_request(request):

    # first, try to login using the api_key url arg
    api_key = request.args.get('api_key')
    if api_key:
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return user

    # next, try to login using Basic Auth
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        try:
            api_key = base64.b64decode(api_key)
        except TypeError:
            pass
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return user

    # finally, return None if both methods did not login the user
    return None



import metaflask.userapi, metaflask.views
#import metaflask.msfapi 