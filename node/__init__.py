from sqlalchemy import Column, String, Integer

import storage


class Node(storage.Base):
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

def add_node(node):
    storage.insert(node)

def count():
    return storage.count(Node)

def get_my_node():
    pass

def get_all():
    return storage.get_all(Node)