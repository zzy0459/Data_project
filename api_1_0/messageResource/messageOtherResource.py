#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Resource
from flask_restful import Resource, reqparse
from flask import jsonify, Response, stream_with_context
from service.messageService import MessageService
from controller.messageController import MessageController
from utils import commons
from utils.response_code import RET, error_map_EN
import json

class MessageOtherResource(Resource):
	@classmethod
	def getChatMessage(cls, AutoID=None, ConversationID=None):
		print("getchatmessage")
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
		# parser.add_argument('ConversationID', location='args', required=True,help='ConversationID参数类型不正确或缺失')
		kwargs = parser.parse_args()
		kwargs = commons.put_remove_none(**kwargs)

		res = MessageService.getChatMeaasge(ConversationID=ConversationID, Content=kwargs.get('Content'))

		def generate(text):
			# 生成流式数据
			# 将文本数据分成多行（或按需要分割），然后逐行发送
			for line in text.split('。'):  # 按句号分割
				if line.strip():  # 确保不发送空行
					yield f"data: {line.strip()}。\n\n"  # 每行以 data: 开头，并以双换行结束
			# 发送结束消息
			yield 'data: [DONE] \n\n'

		return Response(stream_with_context(generate(res['data'])), content_type='text/event-stream')

		# res = MessageService.getChatMeaasge(**kwargs)
		# print("res",res)
		# return jsonify(code=RET.OK, message=error_map_EN[RET.OK], data=res['data'])

	@classmethod
	def getHistoryMessage(cls, AutoID=None):
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

