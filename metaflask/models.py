#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: harmoN
# @Date:   2015-02-13 16:27:12
# @Last Modified by:   harmoN
# @Last Modified time: 2015-02-15 10:57:34
from flask import g
from flask.ext.sqlalchemy import SQLAlchemy
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature
from passlib.apps import custom_app_context as pwd_context
from metaflask import app
import config

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), index=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(10), index=True)
    create_date = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True, unique=False)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration = 600):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'id': self.id })

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['id'])
        return user

    def __init__(self, username, password, role):
        self.username = username
        self.role = role
        self.password_hash = pwd_context.encrypt(password)

