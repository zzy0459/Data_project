#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Api

from . import message_blueprint
from api_1_0.messageResource.messageResource import MessageResource
from api_1_0.messageResource.messageOtherResource import MessageOtherResource

api = Api(message_blueprint)

api.add_resource(MessageResource, '/message/<AutoID>', '/message', endpoint='Message')

@message_blueprint.route('/message/getChatMessage/<int:ConversationID>', methods=['GET'], endpoint='getChatMessage')
def getChatMessage(ConversationID):
    return MessageOtherResource.getChatMessage(ConversationID=ConversationID)

@message_blueprint.route('/message/getHistoryMessage/<int:ConversationID>', methods=['GET'], endpoint='getHistoryMessage')
def getHistoryMessage(ConversationID):
    return MessageOtherResource.getHistoryMessage(ConversationID=ConversationID)