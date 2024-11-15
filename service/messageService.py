#!/usr/bin/env python
# -*- coding:utf-8 -*-

from controller.messageController import MessageController
from service.spark_ai import SparkAIWrapper
from sparkai.core.messages import ChatMessage
import datetime

from flask import jsonify

import math
from app import db

from utils import commons
from utils.response_code import RET, error_map_EN
from utils.loggings import loggings
import math

from app import db
import datetime
import math
import json

from sqlalchemy import or_

from app import db

from utils import commons
from utils.response_code import RET, error_map_EN
from utils.loggings import loggings


from utils import commons
from utils.response_code import RET, error_map_EN
from utils.loggings import loggings
class MessageService(MessageController):
    @classmethod
    def getChatMeaasge(cls, **kwargs):
        try:

            kwargs1={'ConversationID':kwargs['ConversationID']}
            results = MessageController.get(**kwargs1)

            text = [
                # ChatMessage(role="system", content="你现在扮演李白，你豪情万丈，狂放不羁；接下来请用李白的口吻和用户对话。"), # 设置对话背景或者模型角色
                # ChatMessage(role="user", content="之前的问题"),
                # ChatMessage(role="assistant", content="之前的回答"), ...
            ]
            role="user"
            if results['data'] is not None:
                for i in results['data']:
                    if i['User'] == -1:
                        role = "system"
                    elif i['User'] == 0:
                        role = "assistant"
                    else:
                        role = "user"
                    # kw2={'role': role,"content":i['Content']}
                    text.append(ChatMessage(role=role, content=i['Content']))
            # kw3={"role": "user", "content": kwargs['Content']}
            new_message =kwargs['Content']
            wrapper = SparkAIWrapper()
            response = wrapper.send_message_with_context(new_message, text)
            res1=response.generations[0][0].text
            MessageController.add(**{'AutoID':results['data'][-1]['AutoID']+1,'ConversationID': kwargs['ConversationID'], 'User': 1, 'Content': kwargs['Content'],'Number':results['data'][-1]['Number']+1})
            MessageController.add(**{'AutoID':results['data'][-1]['AutoID']+2,'ConversationID': kwargs['ConversationID'], 'User': 0, 'Content': res1,'Number':results['data'][-1]['Number']+2})
            return {'code': RET.OK, 'message': error_map_EN[RET.OK],
                    'data': res1}
        except Exception as e:
            pass
            # loggings.exception(1, e)
            # return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()
        # return cls.getFileExplain(**kwargs)

