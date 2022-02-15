from sqlalchemy.sql.sqltypes import Integer, String, Boolean
from sqlalchemy.sql.schema import ForeignKey, Table
from sqlalchemy.orm import *
from db.database import Base
from sqlalchemy import Column

class DbAssociation(Base):
    __tablename__ = 'association'
    user_id = Column(Integer, ForeignKey('user_inf.id'), primary_key=True)
    course_id = Column(Integer, ForeignKey('course_inf.id'), primary_key=True)


class DbUser(Base):
    __tablename__ = 'user_inf'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    courses = relationship('DbCourse', secondary='association')


class DbCourse(Base):
    __tablename__ = 'course_inf'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    rating = Column(Integer)
    files = relationship('DbFile')


class DbFile(Base):
    __tablename__ = 'file_inf'
    name = Column(String, primary_key=True)
    course_id = Column(Integer, ForeignKey('course_inf.id'))
