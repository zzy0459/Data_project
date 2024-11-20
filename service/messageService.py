#!/usr/bin/env python
# -*- coding:utf-8 -*-

from cryptography.fernet import Fernet
import base64
import os

from controller.messageController import MessageController
from service.spark_ai import SparkAIWrapper
from sparkai.core.messages import ChatMessage
from app import db
import hashlib
from flask import jsonify
from app import db
from utils import commons

import datetime
import math
import json
from sqlalchemy import or_
from app import db

from utils.response_code import RET, error_map_EN
from utils.loggings import loggings

class MessageService(MessageController):
    # 固定的密钥用于加密和解密
    ENCRYPTION_KEY = 'your-encryption-key'

    @staticmethod
    def encrypt(content, key):
        # 使用异或加密
        return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(content))

    @staticmethod
    def decrypt(encrypted_content, key):
        # 使用异或解密
        return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(encrypted_content))

    @classmethod
    def getChatMeaasge(cls, **kwargs):
        try:
            kwargs1 = {'ConversationID': kwargs['ConversationID']}
            results = MessageController.get(**kwargs1)

            text = []
            role = "user"
            if results['data'] is not None:
                for i in results['data']:
                    if i['User'] == -1:
                        role = "system"
                    elif i['User'] == 0:
                        role = "assistant"
                    else:
                        role = "user"
                    # 解密内容后添加到上下文中
                    decrypted_content = cls.decrypt(i['Content'], cls.ENCRYPTION_KEY)
                    text.append(ChatMessage(role=role, content=decrypted_content))

            new_message = kwargs['Content']
            wrapper = SparkAIWrapper()
            response = wrapper.send_message_with_context(new_message, text)
            res1 = response.generations[0][0].text
            # 加密新消息后添加到数据库
            encrypted_new_message = cls.encrypt(kwargs['Content'], cls.ENCRYPTION_KEY)
            encrypted_res1 = cls.encrypt(res1, cls.ENCRYPTION_KEY)

            print("results",results)
            if not results['data']:  # 如果 results['data'] 为空
                auto_id = 1
                number = 1  # 也可以将 Number 设置为 1
            else:
                auto_id = results['data'][-1]['AutoID'] + 1
                number = results['data'][-1]['Number'] + 1
            MessageController.add(**{
                'AutoID': auto_id,
                'ConversationID': kwargs['ConversationID'],
                'User': 1,
                'Content': encrypted_new_message,
                'Number': number
            })
            MessageController.add(**{
                'AutoID': auto_id + 1,
                'ConversationID': kwargs['ConversationID'],
                'User': 0,
                'Content': encrypted_res1,
                'Number': number + 1
            })
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': res1}
        except Exception as e:
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()



