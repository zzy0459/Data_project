#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Resource
from flask_restful import Resource, reqparse
from flask import jsonify
from service.messageService import MessageService
from controller.messageController import MessageController
from utils import commons
from utils.response_code import RET, error_map_EN
import json

class MessageOtherResource(Resource):
	@classmethod
	def getChatMeaasge(cls, AutoID=None):
		if AutoID:
			kwargs = {
				'AutoID': AutoID
			}

			res = MessageController.get(**kwargs)
			if res['code'] == RET.OK:
				return jsonify(code=res['code'], message=res['message'], data=res['data'])
			else:
				return jsonify(code=res['code'], message=res['message'], data=res['data'])

		parser = reqparse.RequestParser()
		parser.add_argument('Content', location='args', required=False, help='Content参数类型不正确或缺失')
		parser.add_argument('ConversationID', location='args', required=False,
							help='ConversationID参数类型不正确或缺失')
		kwargs = parser.parse_args()
		kwargs = commons.put_remove_none(**kwargs)

		res = MessageService.getChatMeaasge(**kwargs)
		return jsonify(code=RET.OK, message=error_map_EN[RET.OK], data=res['data'])

	@classmethod
	def getHistoryMeaasge(cls, AutoID=None):
		if AutoID:
			kwargs = {
				'AutoID': AutoID
			}

			res = MessageController.get(**kwargs)
			if res['code'] == RET.OK:
				return jsonify(code=res['code'], message=res['message'], data=res['data'])
			else:
				return jsonify(code=res['code'], message=res['message'], data=res['data'])

		parser = reqparse.RequestParser()
		parser.add_argument('ConversationID', location='args', required=False,
							help='ConversationID参数类型不正确或缺失')
		kwargs = parser.parse_args()
		kwargs = commons.put_remove_none(**kwargs)

		res = MessageController.get(**kwargs)
		return jsonify(code=RET.OK, message=error_map_EN[RET.OK], data=res['data'])

