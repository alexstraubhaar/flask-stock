from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property
from stck.database import Base
from . import bcrypt

class User(Base):
    __tablename__='users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    pwd = Column(String(128))

    def __init__(self, username=None, pwd=None):
        self.username = username
        self.pwd = set_password(pwd)

    @hybrid_property
    def password(self):
        return self.pwd

    @password.setter
    def set_password(self, plaintext):
        self.pwd = bcrypt.generate_password_hash(plaintext)

    def __repr__(self):
        return '<User %r>' % self.name
