#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: harmoN
# @Date:   2015-02-13 16:27:12
# @Last Modified by:   harmoN
# @Last Modified time: 2015-02-15 10:57:34
from flask import g
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature
from passlib.apps import custom_app_context as pwd_context
from metaflask import app

db = SQLAlchemy(app)

def is_sequence(arg):
    return (not hasattr(arg, "strip") and
            hasattr(arg, "__getitem__") or
            hasattr(arg, "__iter__"))
    

def _role_find_or_create(r):
    role = Role.query.filter_by(name=r).first()
    if not(role):
        role = Role(name=r)
        db.session.add(role)
    return role

'''
user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))
    )
'''

user_role_table = db.Table('user_role',
                           db.Column(
                               'user_id', db.Integer, db.ForeignKey('user.id')),
                           db.Column(
                           'role_id', db.Integer, db.ForeignKey('role.id'))
                           )


role_ability_table = db.Table('role_ability',
                              db.Column(
                                  'role_id', db.Integer, db.ForeignKey('role.id')),
                              db.Column(
                              'ability_id', db.Integer, db.ForeignKey('ability.id'))
                              )



class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    abilities = db.relationship(
        'Ability', secondary=role_ability_table, backref='roles')

    def __init__(self, name):
        self.name = name.lower()

    def add_abilities(self, *abilities):
        for ability in abilities:
            existing_ability = Ability.query.filter_by(
                name=ability).first()
            if not existing_ability:
                existing_ability = Ability(ability)
                db.session.add(existing_ability)
                db.session.commit()
            self.abilities.append(existing_ability)

    def remove_abilities(self, *abilities):
        for ability in abilities:
            existing_ability = Ability.query.filter_by(name=ability).first()
            if existing_ability and existing_ability in self.abilities:
                self.abilities.remove(existing_ability)

    def __repr__(self,name):
        print "<Role: {} >".format(name) 

    def __str__(self):
        return self.name


class Ability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)

    def __init__(self, name):
        self.name = name.lower()

    def __repr__(self):
        return '<Ability {}>'.format(self.name)

    def __str__(self):
        return self.name



''' old user model..
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40))
    password_hash = db.Column(db.String(128))
    active = db.Column(db.Boolean, default=True, unique=False)
    api_key = db.Column(db.String(128))
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=user_roles, 
            primaryjoin=(user_roles.c.user_id == id), 
            secondaryjoin=(user_roles.c.role_id == role_id), 
            backref=db.backref('user_roles', lazy='dynamic'), 
            lazy='dynamic')

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration = 600):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'id': self.api_key })

    def add_role(self, role):
        if not self.check_role:
            self.roles.append(role)
            return self
    
    def del_role(self, role):
          if self.check_role:
            self.roles.remove(role)
            return self

    def check_role(self, role):
        return self.roles.filter(user_roles.c.role_id == user.id).count() > 0

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['api_key'])
        return user

    def __init__(self, **kwargs):
        if kwargs.get('username'):
            self.username = kwargs.get('username')
        if kwargs.get('password'):
            self.password_hash = pwd_context.encrypt(kwargs.get('password'))
        if self.roles == None:
            roles = []

    def __repr__(self, username):
        print "<User: {} >".format(username) 

     def __str__(self):
        return self.username

'''


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40))
    password_hash = db.Column(db.String(128))
    _roles = db.relationship(
        'Role', secondary=user_role_table, backref='users')
    type = db.Column(db.String(50))

    roles = association_proxy('_roles', 'name', creator=_role_find_or_create)

    __mapper_args__ = {
        'polymorphic_identity': 'usermixin',
        'polymorphic_on': type
    }

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration = 600):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'id': self.api_key })

    def __init__(self, username, password, roles=None, default_role='user'):
        self.username = username
        self.password_hash = pwd_context.encrypt(password)
        # If only a string is passed for roles, convert it to a list containing
        # that string
        if roles and isinstance(roles, basestring):
            roles = [roles]

        # If a sequence is passed for roles (or if roles has been converted to
        # a sequence), fetch the corresponding database objects and make a list
        # of those.
        if roles and is_sequence(roles):
            self.roles = roles
        # Otherwise, assign the default 'user' role. Create that role if it
        # doesn't exist.
        elif default_role:
            self.roles = [default_role]

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def add_roles(self, *roles):
        self.roles.extend([role for role in roles if role not in self.roles])

    def remove_roles(self, *roles):
        self.roles = [role for role in self.roles if role not in roles]

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User {}>'.format(self.id)
    
    def __str__(self):
        return self.username


