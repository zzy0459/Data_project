#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import math
import json

from sqlalchemy import or_

from app import db
from models.message import Message
from utils import commons
from utils.response_code import RET, error_map_EN
from utils.loggings import loggings
from models import BaseModel

ENCRYPTION_KEY = 'your-encryption-key'

def decrypt(encrypted_content, key):
    # 使用异或解密文本
    return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(encrypted_content))


class MessageController(Message,BaseModel):

    # add
    @classmethod
    def add(cls, **kwargs):
        
        try:
            model = Message(
                MessageID=kwargs.get('MessageID'),
                Content=kwargs.get('Content'),
                ConversationID=kwargs.get('ConversationID'),
                User=kwargs.get('User'),
                Number=kwargs.get('Number'),
                
            )
            db.session.add(model)
            db.session.commit()
            results = {
                'add_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'AutoID': model.AutoID,
                
            }
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}
            
        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()

    # get
    @classmethod
    def get(cls, **kwargs):
        try:
            filter_list = []
            if kwargs.get('AutoID'):
                filter_list.append(cls.AutoID == kwargs['AutoID'])
            else:
                if kwargs.get('ConversationID') is not None:
                    filter_list.append(cls.ConversationID == kwargs.get('ConversationID'))
                if kwargs.get('AutoID') is not None:
                    filter_list.append(cls.AutoID == kwargs.get('AutoID'))
                if kwargs.get('MessageID') is not None:
                    filter_list.append(cls.MessageID == kwargs.get('MessageID'))
                if kwargs.get('Content'):
                    filter_list.append(cls.Content == kwargs.get('Content'))
                if kwargs.get('User') is not None:
                    filter_list.append(cls.User == kwargs.get('User'))
                if kwargs.get('Number') is not None:
                    filter_list.append(cls.Number == kwargs.get('Number'))
                

            page = int(kwargs.get('Page', 1))
            size = int(kwargs.get('Size', 10))
            
            message_info = db.session.query(cls).filter(*filter_list)

            for message in message_info:
                if hasattr(message, 'Content') and message.Content is not None:
                    message.Content = decrypt(message.Content,ENCRYPTION_KEY)
            
            count = message_info.count()
            pages = math.ceil(count / size)
            message_info = message_info.limit(size).offset((page - 1) * size).all()
   
            #results = commons.query_to_dict(message_info)
            results = cls.to_dict(message_info)
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'totalCount': count, 'totalPage': pages, 'data': results}
            
        except Exception as e:
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()

    # delete
    @classmethod
    def delete(cls, **kwargs):
        try:
            filter_list = []
            if kwargs.get('AutoID'):
                primary_key_list = []
                for primary_key in str(kwargs.get('AutoID')).replace(' ', '').split(','):
                    primary_key_list.append(cls.AutoID == primary_key)
                filter_list.append(or_(*primary_key_list))
                
            else:
                if kwargs.get('AutoID') is not None:
                    filter_list.append(cls.AutoID == kwargs.get('AutoID'))
                if kwargs.get('MessageID') is not None:
                    filter_list.append(cls.MessageID == kwargs.get('MessageID'))
                if kwargs.get('Content'):
                    filter_list.append(cls.Content == kwargs.get('Content'))
                if kwargs.get('ConversationID') is not None:
                    filter_list.append(cls.ConversationID == kwargs.get('ConversationID'))
                if kwargs.get('User') is not None:
                    filter_list.append(cls.User == kwargs.get('User'))
                if kwargs.get('Number') is not None:
                    filter_list.append(cls.Number == kwargs.get('Number'))
                
            res = db.session.query(cls).filter(*filter_list).with_for_update()

            results = {
                'delete_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'AutoID': []
            }
            for query_model in res.all():
                results['AutoID'].append(query_model.AutoID)

            res.delete()
            db.session.commit()

            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}

        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()

    # update
    @classmethod
    def update(cls, **kwargs):
        try:
            
            
            filter_list = []
            filter_list.append(cls.AutoID == kwargs.get('AutoID'))
            
            res = db.session.query(cls).filter(*filter_list).with_for_update()
            if res.first():
                results = {
                    'update_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'AutoID': res.first().AutoID,
                
                }
                
                res.update(kwargs)
                db.session.commit()
            else:
                results = {
                    'error': 'data dose not exist'
                }
            
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}

        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()

    # batch add
    @classmethod
    def add_list(cls, **kwargs):
        param_list = kwargs.get('MessageList')
        model_list = []
        for param_dict in param_list:
            
            model = Message(
                MessageID=param_dict.get('MessageID'),
                Content=param_dict.get('Content'),
                ConversationID=param_dict.get('ConversationID'),
                User=param_dict.get('User'),
                Number=param_dict.get('Number'),
                
            )
            model_list.append(model)
        
        try:
            db.session.add_all(model_list)
            db.session.commit()
            results = {
                'added_records': [],
                'add_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            for model in model_list:
                added_record = {}
                added_record['AutoID'] = model.AutoID
                
                results['added_records'].append(added_record)
                
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}
            
        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()
