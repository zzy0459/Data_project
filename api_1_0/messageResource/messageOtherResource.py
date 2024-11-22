#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Resource
from flask_restful import Resource, reqparse
from flask import jsonify, Response, stream_with_context

from service.conversationService import ConversationService
from service.messageService import MessageService
from controller.messageController import MessageController
from utils import commons
from utils.response_code import RET, error_map_EN
import json

class MessageOtherResource(Resource):
	@classmethod
	def getChatMessage(cls, ConversationID=None):
		print("getchatmessage")
		"""
		if AutoID:
			kwargs = {
				'AutoID': AutoID
			}

			res = MessageController.get(**kwargs)
			if res['code'] == RET.OK:
				return jsonify(code=res['code'], message=res['message'], data=res['data'])
			else:
				return jsonify(code=res['code'], message=res['message'], data=res['data'])
		"""
		parser = reqparse.RequestParser()
		parser.add_argument('Content', location='args', required=False, help='Content参数类型不正确或缺失')
		# parser.add_argument('ConversationID', location='args', required=True,help='ConversationID参数类型不正确或缺失')
		kwargs = parser.parse_args()
		kwargs = commons.put_remove_none(**kwargs)

		res = MessageService.getChatMeaasge(ConversationID=ConversationID, Content=kwargs.get('Content'))

		def generate(text):
			# 生成流式数据
			# 将文本数据分成多行（或按需要分割），然后逐行发送
			if '。' in text:
				for line in text.split('。'):  # 按句号分割
					if line.strip():  # 确保不发送空行
						yield f"data: {line.strip()}。\n\n"  # 每行以 data: 开头，并以双换行结束
			else:
				for line in text.split('.'):  # 按句号分割
					if line.strip():  # 确保不发送空行
						yield f"data: {line.strip()}.\n\n"  # 每行以 data: 开头，并以双换行结束
			# 发送结束消息
			yield 'data: [DONE]\n\n'

		return Response(stream_with_context(generate(res['data'])), content_type='text/event-stream')

		# res = MessageService.getChatMeaasge(**kwargs)
		# print("res",res)
		# return jsonify(code=RET.OK, message=error_map_EN[RET.OK], data=res['data'])

	@classmethod
	def getHistoryMessage(cls, ConversationID=None):
		"""
		if AutoID:
			kwargs = {
				'AutoID': AutoID
			}

			res = MessageController.get(**kwargs)
			if res['code'] == RET.OK:
				return jsonify(code=res['code'], message=res['message'], data=res['data'])
			else:
				return jsonify(code=res['code'], message=res['message'], data=res['data'])
		"""
		parser = reqparse.RequestParser()
		# parser.add_argument('ConversationID', location='args', required=False,help='ConversationID参数类型不正确或缺失')
		kwargs = parser.parse_args()
		kwargs = commons.put_remove_none(**kwargs)

		res = MessageController.get(ConversationID=ConversationID)

		data = res['data']

		title = ConversationService.get_title(ConversationID=ConversationID)['data']

		# 转换数据
		result = {
			"id": data[0]['ConversationID'],
			"title": title,
			"data": {
				"convs": []
			}
		}

		for message in data:
			if message['User'] == 1:
				result['data']['convs'].append({
					"speaker": "human",
					"speech": message['Content']
				})
			else:
				# 如果是AI的回复，查看是否已经存在speeches
				if result['data']['convs'] and result['data']['convs'][-1]['speaker'] == "ai":
					result['data']['convs'][-1]['speeches'].append(message['Content'])
				else:
					result['data']['convs'].append({
						"speaker": "ai",
						"speeches": [message['Content']]
					})
		print("history data",result)
		# return jsonify(code=RET.OK, message=error_map_EN[RET.OK], data=res['data'])
		return result

