#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Api

from . import message_blueprint
from api_1_0.messageResource.messageResource import MessageResource
from api_1_0.messageResource.messageOtherResource import MessageOtherResource

api = Api(message_blueprint)

api.add_resource(MessageResource, '/message/<AutoID>', '/message', endpoint='Message')

@message_blueprint.route('/message/getChatMeaasge', methods=['GET'], endpoint='getChatMeaasge')
def getChatMeaasge():
    return MessageOtherResource.getChatMeaasge()

@message_blueprint.route('/message/getHistoryMeaasge', methods=['GET'], endpoint='getHistoryMeaasge')
def getHistoryMeaasge():
    return MessageOtherResource.getHistoryMeaasge()