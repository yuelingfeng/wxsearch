#coding=utf-8
from flask_sqlalchemy import SQLAlchemy
import datetime
from .exts import db

class BaseModel():

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}



class Users(db.Model,BaseModel):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company = db.Column(db.Integer,db.ForeignKey('company.id'))
    phone = db.Column(db.String(13), nullable=False)
    name = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(32))
    wxid = db.Column(db.String(28), nullable=False)
    state = db.Column(db.String(1), default='N')
    createdatetime = db.Column(db.DateTime, default=datetime.datetime.now)



class Company(db.Model,BaseModel):
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50),nullable = False)
    sn = db.Column(db.String(8),nullable = False)
    ipaddress =db.Column(db.String(23), nullable=False)
    state = db.Column(db.String(1), default='N') 
    duedate = db.Column(db.DateTime, default=datetime.datetime.now)
    createdatetime = db.Column(db.DateTime, default=datetime.datetime.now)
    user = db.relationship('Users',backref='lazzy')