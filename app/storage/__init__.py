from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

Base = declarative_base()

engine = create_engine('sqlite:///mychain1.db?check_same_thread=False')
Base.metadata.bind = engine
DBSession = scoped_session(sessionmaker(bind=engine))
session = DBSession()


def init():
	Base.metadata.create_all(engine)


def insert(obj):
	session.add(obj)
	session.commit()


def insert_or_update(obj, cond):
	if session.query(obj.__class__).filter(cond).first():
		return
	else:
		insert(obj)


def get(clz, **kwargs):
	return session.query(clz).filter_by(**kwargs).first()


def count(clz):
	return session.query(clz).count()


def remove(obj):
	session.delete(obj)
	session.commit()


def get_all(clz):
	return session.query(clz).all()


def remove_all(clz):
	session.query(clz).delete()
	session.commit()
