#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import request
from flask_restful import Api

from . import conversation_blueprint
from api_1_0.conversationResource.conversationResource import ConversationResource
from api_1_0.conversationResource.conversationOtherResource import ConversationOtherResource

api = Api(conversation_blueprint)

api.add_resource(ConversationResource, '/conversation/<AutoID>', '/conversation', endpoint='Conversation')

@conversation_blueprint.route('/conversation/Evaluate/<int:ConversationID>', methods=['PUT'], endpoint='Evaluate')
def Evaluate(ConversationID):
    return ConversationOtherResource.Evaluate(ConversationID)

@conversation_blueprint.route('/conversation/add_conversation', methods=['POST'], endpoint='add_conversation')
def add_conversation():
    return ConversationOtherResource.add_conversation()

@conversation_blueprint.route('/conversation/get_title/<int:ConversationID>', methods=['GET'], endpoint='get_title')
def get_title(ConversationID):
    return ConversationOtherResource.get_title(ConversationID)