import db

my_node = None
my_node_json = None
node_list = None
trust_node_ip = "163.239.27.32"
node_sync = False   # Need to Set FALSE after Test
from sqlalchemy import Column, String, Integer

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

def add_node(node):
    db.insert(node)

def count():
    return db.count(Node)

def get_my_node():
    pass

def get_all():
    return db.get_all(Node)