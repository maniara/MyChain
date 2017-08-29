import json

from sqlalchemy import Column, String, Integer

import db


class Node(db.Base):
    __tablename__ = 'nodes'

    _id = Column(Integer, primary_key=True, autoincrement=True)
    ip_address = Column(String)
    type = Column(String)
    public_key = Column(String)
    private_key = Column(String)

    def __init__(self, ip_address):
        self.type = 'N'
        self.ip_address = ip_address
        self.public_key = ''
        self.private_key = ''

    def __str__(self):
        return self.to_json()

    def to_json(self):
        return json.dumps({
            'type': self.type,
            'ip_address': self.ip_address,
            'pub_key': self.public_key,
            'pri_key': self.private_key
        })

def add_node(node):
    db.insert(node)

def count():
    return db.count(Node)

def get_my_node():
    pass

def get_all():
    return db.get_all(Node)