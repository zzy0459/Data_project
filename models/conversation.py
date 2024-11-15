# coding: utf-8
from . import db, BaseModel


class Conversation(db.Model):
    __tablename__ = 'conversation'

    AutoID = db.Column(db.Integer, primary_key=True)
    ConversationID = db.Column(db.Integer)
    Title = db.Column(db.String(255))
    Satisfaction = db.Column(db.Integer)
    Evaluate_Content = db.Column(db.String(255))
    Persona = db.Column(db.String(255))
    Accuracy = db.Column(db.Integer)
    adaptability = db.Column(db.Integer)
