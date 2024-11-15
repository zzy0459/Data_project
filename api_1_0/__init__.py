#!/usr/bin/env python
# -*- coding:utf-8 -*-

from .apiVersionResource import apiversion_blueprint
from .conversationResource import conversation_blueprint
from .messageResource import message_blueprint


def init_router(app):
    from api_1_0.apiVersionResource import apiversion_blueprint
    app.register_blueprint(apiversion_blueprint, url_prefix="/api_1_0")

    # conversation blueprint register
    from api_1_0.conversationResource import conversation_blueprint
    app.register_blueprint(conversation_blueprint, url_prefix="/api_1_0")
    
    # message blueprint register
    from api_1_0.messageResource import message_blueprint
    app.register_blueprint(message_blueprint, url_prefix="/api_1_0")
    
