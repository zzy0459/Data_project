#!/usr/bin/env python
# -*- coding:utf-8 -*- 

from flask_restful import Resource, reqparse
from flask import jsonify

from controller.messageController import MessageController
from utils import commons
from utils.response_code import RET, error_map_EN
import json


class MessageResource(Resource):

    # get
    @classmethod
    def get(cls, AutoID=None):
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
        parser.add_argument('AutoID', location='args', required=False, help='AutoID参数类型不正确或缺失')
        parser.add_argument('MessageID', location='args', required=False, help='MessageID参数类型不正确或缺失')
        parser.add_argument('Content', location='args', required=False, help='Content参数类型不正确或缺失')
        parser.add_argument('ConversationID', location='args', required=False, help='ConversationID参数类型不正确或缺失')
        parser.add_argument('User', location='args', required=False, help='User参数类型不正确或缺失')
        parser.add_argument('Number', location='args', required=False, help='Number参数类型不正确或缺失')

        parser.add_argument('Page', location='args', required=False, help='Page参数类型不正确或缺失')
        parser.add_argument('Size', location='args', required=False, help='Size参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        res = MessageController.get(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'], data=res['data'], totalPage=res['totalPage'], totalCount=res['totalCount'])
        else:
            return jsonify(code=res['code'], message=res['message'], data=res['data'])


    # delete
    @classmethod
    def delete(cls, AutoID=None):
        if AutoID:
            kwargs = {
                'AutoID': AutoID
            }

        else:
            return jsonify(code=RET.PARAMERR, message=error_map_EN[RET.PARAMERR], data='id不能为空')

        res = MessageController.delete(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])


    # put
    @classmethod
    def put(cls, AutoID):
        if not AutoID:
            return jsonify(code=RET.NODATA, message='primary key missed', error='primary key missed')

        parser = reqparse.RequestParser()
        parser.add_argument('MessageID', location='form', required=False, help='MessageID参数类型不正确或缺失')
        parser.add_argument('Content', location='form', required=False, help='Content参数类型不正确或缺失')
        parser.add_argument('ConversationID', location='form', required=False, help='ConversationID参数类型不正确或缺失')
        parser.add_argument('User', location='form', required=False, help='User参数类型不正确或缺失')
        parser.add_argument('Number', location='form', required=False, help='Number参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)
        kwargs['AutoID'] = AutoID

        res = MessageController.update(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])


    # add
    @classmethod
    def post(cls):
        '''
        MessageList: Pass in values in JSON format to batch add
        eg.[{k1:v1,k2:v2,...},...]
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('MessageList', type=str, location='form', required=False, help='MessageList参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        if kwargs.get('MessageList'):
            kwargs['MessageList'] = json.loads(kwargs['MessageList'])
            for data in kwargs['MessageList']:
                for key in []:
                    data.pop(key, None)
            res = MessageController.add_list(**kwargs)

        else:
            parser.add_argument('MessageID', location='form', required=False, help='MessageID参数类型不正确或缺失')
            parser.add_argument('Content', location='form', required=False, help='Content参数类型不正确或缺失')
            parser.add_argument('ConversationID', location='form', required=False, help='ConversationID参数类型不正确或缺失')
            parser.add_argument('User', location='form', required=False, help='User参数类型不正确或缺失')
            parser.add_argument('Number', location='form', required=False, help='Number参数类型不正确或缺失')

            kwargs = parser.parse_args()
            kwargs = commons.put_remove_none(**kwargs)

            res = MessageController.add(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])
