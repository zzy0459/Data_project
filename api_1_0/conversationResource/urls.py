#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Api

from . import conversation_blueprint
from api_1_0.conversationResource.conversationResource import ConversationResource
from api_1_0.conversationResource.conversationOtherResource import ConversationOtherResource

api = Api(conversation_blueprint)

api.add_resource(ConversationResource, '/conversation/<AutoID>', '/conversation', endpoint='Conversation')

@conversation_blueprint.route('/conversation/Evaluate', methods=['GET'], endpoint='Evaluate')
def Evaluate():
    return ConversationOtherResource.Evaluate()

@conversation_blueprint.route('/conversation/add_conversation', methods=['POST'], endpoint='add_conversation')
def add_conversation():
    return ConversationOtherResource.add_conversation()

@conversation_blueprint.route('/conversation/get_title', methods=['GET'], endpoint='get_title')
def get_title():
    return ConversationOtherResource.get_title()