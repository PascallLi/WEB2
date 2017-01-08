from . import ModelMixin
from . import db
from . import timestamp

# 来自user.py粘贴过来，建立之后需要新建表，init migrate upgrade
class Node(db.Model, ModelMixin):
    __tablename__ = 'nodes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.String())
    # has relationship with topic
    topics = db.relationship('Topic', backref="node")

    def __init__(self, form):
        self.name = form.get('name', '')
