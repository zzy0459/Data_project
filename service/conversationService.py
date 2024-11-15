#!/usr/bin/env python
# -*- coding:utf-8 -*-

from controller.conversationController import ConversationController
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

class ConversationService(ConversationController):
    @classmethod
    def Evaluate(cls, **kwargs):
        try:

            kwargs1 = {'AutoID': kwargs['ConversationID'],'ConversationID': kwargs['ConversationID'],'Satisfaction': kwargs['Satisfaction'],'Evaluate_Content': kwargs['Evaluate_Content']}
            results = ConversationController.update(**kwargs1)


            return {'code': RET.OK, 'message': error_map_EN[RET.OK],
                    'data': results}
        except Exception as e:
            pass
            # loggings.exception(1, e)
            # return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()
        # return cls.getFileExplain(**kwargs)

    @classmethod
    def add_conversation(cls, **kwargs):
        try:
            print(kwargs)
            kwargs1 = {'ConversationID': kwargs['ConversationID'],
                       'Title': kwargs['Title'], 'Persona': kwargs['Persona']}
            results = ConversationController.add(**kwargs1)
            return {'code': RET.OK, 'message': error_map_EN[RET.OK],
                    'data': results}
        except Exception as e:
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()
        # return cls.getFileExplain(**kwargs)