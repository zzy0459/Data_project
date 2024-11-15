#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse
from flask import jsonify
from service.conversationService import ConversationService
from controller.conversationController import ConversationController
from utils import commons
from utils.response_code import RET, error_map_EN
import json


class ConversationOtherResource(Resource):
	# get
	@classmethod
	def Evaluate(cls, AutoID=None):
		if AutoID:
			kwargs = {
				'AutoID': AutoID
			}

			res = ConversationController.get(**kwargs)
			if res['code'] == RET.OK:
				return jsonify(code=res['code'], message=res['message'], data=res['data'])
			else:
				return jsonify(code=res['code'], message=res['message'], data=res['data'])

		parser = reqparse.RequestParser()
		parser.add_argument('ConversationID', location='args', required=False,
							help='ConversationID参数类型不正确或缺失')
		parser.add_argument('Satisfaction', location='args', required=False, help='Satisfaction参数类型不正确或缺失')
		parser.add_argument('Evaluate_Content', location='args', required=False,
							help='Evaluate_Content参数类型不正确或缺失')


		kwargs = parser.parse_args()
		kwargs = commons.put_remove_none(**kwargs)

		res = ConversationService.Evaluate(**kwargs)
		if res['code'] == RET.OK:
			return jsonify(code=res['code'], message=res['message'], data=res['data'])
		else:
			return jsonify(code=res['code'], message=res['message'], data=res['data'])

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

		if kwargs.get('ConversationList'):
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

			res = ConversationService.add_conversation(**kwargs)

		return jsonify(code=res['code'], message=res['message'], data=res['data'])