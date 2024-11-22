#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse
from flask import jsonify, Response, stream_with_context, request
from service.conversationService import ConversationService
from controller.conversationController import ConversationController
from utils import commons
from utils.response_code import RET, error_map_EN
import json


class ConversationOtherResource(Resource):
	# get
	@classmethod
	def Evaluate(cls, ConversationID=None):
		"""
		if AutoID:
			kwargs = {
				'AutoID': AutoID
			}

			res = ConversationController.get(**kwargs)
			if res['code'] == RET.OK:
				return jsonify(code=res['code'], message=res['message'], data=res['data'])
			else:
				return jsonify(code=res['code'], message=res['message'], data=res['data'])
		"""
		# 获取所有查询参数
		# params = request.args.to_dict()
		# print("params",params)
		# 获取请求体
		data = request.json
		# print("data",data)

		res = ConversationService.Evaluate(ConversationID = ConversationID, suitable=data['suitable'])
		# print("res",res)
		if res['code'] == RET.OK:
			return jsonify(message="Rating updated successfully")
			# return jsonify(code=res['code'], message=res['message'], data=res['data'])
		else:
			return jsonify(message=res['message'])
			# return jsonify(code=res['code'], message=res['message'], data=res['data'])


	@classmethod
	def add_conversation(cls):
		'''
        ConversationList: Pass in values in JSON format to batch add
        eg.[{k1:v1,k2:v2,...},...]
        '''
		parser = reqparse.RequestParser()

		parser.add_argument('ConversationList', type=str, location='form', required=False,
							help='ConversationList参数类型不正确或缺失')

		kwargs = parser.parse_args()
		kwargs = commons.put_remove_none(**kwargs)
		"""
		if kwargs.get('ConversationList'):
			print("'ConversationList'", kwargs['ConversationList'])
			kwargs['ConversationList'] = json.loads(kwargs['ConversationList'])
			for data in kwargs['ConversationList']:
				for key in []:
					data.pop(key, None)
			res = ConversationController.add_list(**kwargs)

		else:
			
			parser.add_argument('ConversationID', location='form', required=False,
								help='ConversationID参数类型不正确或缺失')
			parser.add_argument('Title', location='form', required=False, help='Title参数类型不正确或缺失')
			parser.add_argument('Satisfaction', location='form', required=False,
								help='Satisfaction参数类型不正确或缺失')
			parser.add_argument('Evaluate_Content', location='form', required=False,
								help='Evaluate_Content参数类型不正确或缺失')
			parser.add_argument('Persona', location='form', required=False, help='Persona参数类型不正确或缺失')
			
			kwargs = parser.parse_args()
			kwargs = commons.put_remove_none(**kwargs)
		"""
		res = ConversationService.add_conversation(**kwargs)

		#return jsonify(code=res['code'], message=res['message'], data=res['data'])
		if 'data' in res['data'].keys():
			return jsonify({'data':res['data']['data']['ConversationID']})
		else:
			return jsonify({})

	@classmethod
	def get_title(cls, ConversationID=None):

		"""
		parser = reqparse.RequestParser()

		parser.add_argument('ConversationID', location='args', required=False,
							help='ConversationID参数类型不正确或缺失')


		kwargs = parser.parse_args()
		kwargs = commons.put_remove_none(**kwargs)
		"""
		res = ConversationService.get_title(ConversationID=ConversationID)

		def generate(text):
			# 生成流式数据
			yield f"data: {text}\n\n"  # 每行以 data: 开头，并以双换行结束
			# 发送结束消息
			yield 'data: [DONE]\n\n'
		"""
			if res['code'] == RET.OK:
				return jsonify(code=res['code'], message=res['message'], data=res['data'])
			else:
				return jsonify(code=res['code'], message=res['message'], data=res['data'])
			"""
		return Response(stream_with_context(generate(res['data'])), content_type='text/event-stream')
