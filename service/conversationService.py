#!/usr/bin/env python
# -*- coding:utf-8 -*-
import random

from controller.conversationController import ConversationController
from controller.messageController import MessageController
from service.spark_ai import SparkAIWrapper
from sparkai.core.messages import ChatMessage
import datetime
from flask import jsonify
from utils import commons
from utils.response_code import RET, error_map_EN
from utils.loggings import loggings
import math
from app import db

import json
from sqlalchemy import or_


class ConversationService(ConversationController):
    # 一个固定的密钥用于加密和解密
    ENCRYPTION_KEY = 'your-encryption-key'

    @staticmethod
    def encrypt(content, key):
        # 使用异或加密文本
        return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(content))

    @staticmethod
    def decrypt(encrypted_content, key):
        # 使用异或解密文本
        return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(encrypted_content))

    @classmethod
    def get_title(cls, **kwargs):
        try:
            kwargs1 = {
                'AutoID': kwargs['ConversationID'],
                'ConversationID': kwargs['ConversationID'],
            }
            results = ConversationController.get(**kwargs1)
            if results['data']:
                res = results['data'][0]['Title']
            else:
                res = "New chat"
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': res}
        except Exception as e:
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()

    @classmethod
    def Evaluate(cls, **kwargs):
        try:
            res=ConversationController.get(AutoID=kwargs['ConversationID'])
            res1=res['data'][0]['Satisfaction']
            kwargs1 = {
                'AutoID': kwargs['ConversationID'],
                'ConversationID': kwargs['ConversationID'],
                'Satisfaction': kwargs['Satisfaction']+res1,
                'Evaluate_Content': kwargs['Evaluate_Content']
            }
            results = ConversationController.update(**kwargs1)
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}
        except Exception as e:
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()

    @classmethod
    def add_conversation(cls, **kwargs):
        try:
            print(kwargs)
            title = "New chat"
            persona = "human"
            # conversation_id = kwargs.get('ConversationID', str(random.randint(100000, 999999)))
            # Title和Persona加密
            encrypted_title = cls.encrypt(title, cls.ENCRYPTION_KEY)
            encrypted_persona = cls.encrypt(persona, cls.ENCRYPTION_KEY)
            kwargs1 = {
                # 'ConversationID': conversation_id,
                'Title': encrypted_title,
                'Persona': encrypted_persona
            }
            results = ConversationController.add(**kwargs1)
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}
        except Exception as e:
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()
