#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import math
import json
import random

from sqlalchemy import or_

from app import db
from models.conversation import Conversation
from utils import commons
from utils.response_code import RET, error_map_EN
from utils.loggings import loggings
from models import BaseModel


class ConversationController(Conversation,BaseModel):

    # add
    @classmethod
    def add(cls, **kwargs):
        try:
            # 检查id是否重复
            while True:
                conversation_id = str(random.randint(100000000, 999999999))
                existing_conversation = db.session.query(Conversation).filter_by(
                    ConversationID=conversation_id).first()
                if existing_conversation:
                    continue
                else:
                    break

            model = Conversation(
                ConversationID=conversation_id,
                Title=kwargs.get('Title'),
                Satisfaction=kwargs.get('Satisfaction'),
                Evaluate_Content=kwargs.get('Evaluate_Content'),
                Persona=kwargs.get('Persona'),
                Accuracy=kwargs.get('Accuracy'),
                adaptability=kwargs.get('adaptability'),
                
            )
            db.session.add(model)
            db.session.commit()
            results = {
                'add_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'AutoID': model.AutoID,
                'ConversationID': model.ConversationID
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
                if kwargs.get('AutoID') is not None:
                    filter_list.append(cls.AutoID == kwargs.get('AutoID'))
                if kwargs.get('ConversationID') is not None:
                    filter_list.append(cls.ConversationID == kwargs.get('ConversationID'))
                if kwargs.get('Title'):
                    filter_list.append(cls.Title == kwargs.get('Title'))
                if kwargs.get('Satisfaction') is not None:
                    filter_list.append(cls.Satisfaction == kwargs.get('Satisfaction'))
                if kwargs.get('Evaluate_Content'):
                    filter_list.append(cls.Evaluate_Content == kwargs.get('Evaluate_Content'))
                if kwargs.get('Persona'):
                    filter_list.append(cls.Persona == kwargs.get('Persona'))
                if kwargs.get('Accuracy') is not None:
                    filter_list.append(cls.Accuracy == kwargs.get('Accuracy'))
                if kwargs.get('adaptability') is not None:
                    filter_list.append(cls.adaptability == kwargs.get('adaptability'))
                

            page = int(kwargs.get('Page', 1))
            size = int(kwargs.get('Size', 10))
            
            conversation_info = db.session.query(cls).filter(*filter_list)
            
            count = conversation_info.count()
            pages = math.ceil(count / size)
            conversation_info = conversation_info.limit(size).offset((page - 1) * size).all()
   
            #results = commons.query_to_dict(conversation_info)
            results = cls.to_dict(conversation_info)
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
                if kwargs.get('ConversationID') is not None:
                    filter_list.append(cls.ConversationID == kwargs.get('ConversationID'))
                if kwargs.get('Title'):
                    filter_list.append(cls.Title == kwargs.get('Title'))
                if kwargs.get('Satisfaction') is not None:
                    filter_list.append(cls.Satisfaction == kwargs.get('Satisfaction'))
                if kwargs.get('Evaluate_Content'):
                    filter_list.append(cls.Evaluate_Content == kwargs.get('Evaluate_Content'))
                if kwargs.get('Persona'):
                    filter_list.append(cls.Persona == kwargs.get('Persona'))
                if kwargs.get('Accuracy') is not None:
                    filter_list.append(cls.Accuracy == kwargs.get('Accuracy'))
                if kwargs.get('adaptability') is not None:
                    filter_list.append(cls.adaptability == kwargs.get('adaptability'))
                
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
        param_list = kwargs.get('ConversationList')
        model_list = []
        for param_dict in param_list:
            
            model = Conversation(
                ConversationID=param_dict.get('ConversationID'),
                Title=param_dict.get('Title'),
                Satisfaction=param_dict.get('Satisfaction'),
                Evaluate_Content=param_dict.get('Evaluate_Content'),
                Persona=param_dict.get('Persona'),
                Accuracy=param_dict.get('Accuracy'),
                adaptability=param_dict.get('adaptability'),
                
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
