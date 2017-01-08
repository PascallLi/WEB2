# 来自node.py粘贴过来，增加self.title 和 self.content
from . import ModelMixin
from . import db
from . import timestamp


class Topic(db.Model, ModelMixin):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    content = db.Column(db.String())

    # 增加外键,写完topic与node数据的关系改动后，需要重建数据表
    node_id = db.Column(db.Integer, db.ForeignKey('nodes.id'))

    def __init__(self, form):
        self.title = form.get('title', '')
        self.content = form.get('content', '')
