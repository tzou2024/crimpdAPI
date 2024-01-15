import os
from app import db
import sqlalchemy.orm as so
import sqlalchemy as sa
from typing import Optional, Literal
    
Role_enum = Literal["ROLE_USER", "ROLE_MODERATOR", "ROLE_ADMIN"]

class Users(db.Model):
    id = db.Column('user_id', db.Integer, primary_key=True)
    email = db.Column(db.String(30))
    username = db.Column(db.String(24))
    pwd = db.Column(db.String(64))
    role: so.Mapped[Role_enum] = so.mapped_column(sa.Enum("ROLE_USER", "ROLE_MODERATOR", "ROLE_ADMIN", name="role_enum"))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __init__(self, email, username, pwd):
        self.username = username
        self.email = email
        self.pwd = pwd
        self.role="ROLE_USER"
        

    def __repr__(self):
        return "<User: Username - {}; password - {};>".format(self.username, self.pwd)


    
class InvalidToken(db.Model):
    __tablename__ = "invalid_tokens"
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String)
    def save(self):
        db.session.add(self)
        db.session.commit()
    @classmethod
    def is_invalid(cls, jti):
        """ Determine whether the jti key is on the blocklist return bool"""
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)