from sqlalchemy import Column, String, Integer
import db


class Vote(db.Base):
    __tablename__ = 'votes'

    _id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String)
    delegated_num = Column(Integer)

    def __init__(self, delegated_num):
        self.delegated_num = delegated_num


def save_vote(vote):
    db.insert(vote)

def get_votes():
    return db.get_all(Vote)

def remove_all_vote():
    db.remove_all(Vote)

def get_vote_count():
    return db.count(Vote)
