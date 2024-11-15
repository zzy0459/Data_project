#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint

conversation_blueprint = Blueprint('conversation', __name__)

from . import urls
