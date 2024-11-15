# coding: utf-8
from . import db, BaseModel


class Message(db.Model):
    __tablename__ = 'message'

    AutoID = db.Column(db.Integer, primary_key=True)
    MessageID = db.Column(db.Integer)
    Content = db.Column(db.Text)
    ConversationID = db.Column(db.Integer)
    User = db.Column(db.Integer)
    Number = db.Column(db.Integer)
