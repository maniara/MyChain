from sqlalchemy import Column, String, Integer

from app import storage


class Vote(storage.Base):
    __tablename__ = 'votes'

    _id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String)
    delegated_num = Column(Integer)

    def __init__(self, delegated_num):
        self.delegated_num = delegated_num


def save_vote(vote):
    storage.insert(vote)

def get_votes():
    return storage.get_all(Vote)

def remove_all_vote():
    storage.remove_all(Vote)

def get_vote_count():
    return storage.count(Vote)
