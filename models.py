from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from flask_security import UserMixin, RoleMixin
from flask_security import SQLAlchemyUserDatastore

db = SQLAlchemy()

class RolesUsers(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    role_id = db.Column(db.Integer(), db.ForeignKey("role.id"))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key = True)
    username = db.Column(db.String(), nullable = False, unique = True)
    password = db.Column(db.String(), nullable = True)
    email = db.Column(db.String(), unique = True)
    last_login_at = db.Column(db.DateTime)
    current_login_at = db.Column(db.DateTime)
    current_login_ip = db.Column(db.String(255))
    last_login_ip = db.Column(db.String(255))
    login_count = db.Column(db.Integer)
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles = db.relationship('Role',secondary='roles_users',
                           backref=db.backref('users',lazy='dynamic'))
    sponsor = db.relationship('Sponsor', backref='user')
    influencer = db.relationship('Influencer', backref='user')

    def get_id(self):
        return str(self.id)

class Admin(UserMixin,db.Model):
    id = db.Column(db.Integer(), primary_key = True)   #0
    username = db.Column(db.String(), nullable = False, unique = True)
    password = db.Column(db.String(), nullable = False)
    email = db.Column(db.String(), unique = True)
    admin_id = db.Column(db.Integer(), db.ForeignKey("user.id"), nullable = False)

class Sponsor(db.Model):
    id = db.Column(db.Integer(), primary_key = True)   #1
    company_name = db.Column(db.String(), nullable = False)
    company_budget = db.Column(db.String(), nullable = False)
    username = db.Column(db.String(), nullable = False, unique = True)
    password = db.Column(db.String(), nullable = False)
    email = db.Column(db.String(), unique = True)
    industry = db.Column(db.String(), nullable = False)
    flagged = db.Column(db.Integer(), default = 0) #0-not flagged
    approved = db.Column(db.Integer(), default = 0) #0-not approved
    campaigns = db.relationship('Campaigns', backref = 'sponsor')
    sponsor_id = db.Column(db.Integer(), db.ForeignKey("user.id"), nullable = False)

class Influencer(db.Model):    #2
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(), nullable = False)
    category = db.Column(db.String(), nullable = False)
    reach = db.Column(db.Integer(), nullable = False)
    niche = db.Column(db.String(), nullable = False)
    platform = db.Column(db.String(), nullable = False)
    username = db.Column(db.String(), nullable = False, unique = True)
    password = db.Column(db.String(), nullable = False)
    email = db.Column(db.String(), unique = True)
    flagged = db.Column(db.Integer(), default = 0) 
    adrequests = db.relationship('Adrequests', backref = 'influencer')
    influencer_id = db.Column(db.Integer(), db.ForeignKey("user.id"), nullable = False)

class Campaigns(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(), nullable = False)
    description = db.Column(db.String())
    campaign_budget = db.Column(db.Integer(), nullable = False)
    start_date = db.Column(db.Date(), nullable = False)
    end_date = db.Column(db.Date(), nullable = False)
    visibility = db.Column(db.String(), nullable = False)
    goals = db.Column(db.String(), nullable = False)
    niche = db.Column(db.String(), nullable = False)
    flagged = db.Column(db.Integer(), default = 0)
    sponsor_id = db.Column(db.Integer(), db.ForeignKey("sponsor.id"), nullable = False)
    adrequests = db.relationship('Adrequests', backref = 'campaigns')

class Adrequests(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    messages = db.Column(db.String())
    requirements = db.Column(db.String(), nullable = False)
    status = db.Column(db.String(), nullable = False)
    payment_amt = db.Column(db.Integer(), nullable = False)
    sent_by_sponsor = db.Column(db.Boolean, default=False)
    campaign_id = db.Column(db.Integer(), db.ForeignKey("campaigns.id"), nullable = False)
    influencer_id = db.Column(db.Integer(), db.ForeignKey("influencer.id"), nullable = True)

user_datastore = SQLAlchemyUserDatastore(db, User, Role)