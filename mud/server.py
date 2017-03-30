# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

#==============================================================================
# cause the server to restart itself when python files have been changed on
# disk
#==============================================================================

DEBUG = True

#==============================================================================
# misc imports
#==============================================================================

import os.path, uuid
from mud.config import ROOTDIR
import tornado.web
import tornado.ioloop
from tornado.options import define, options, parse_command_line

#==============================================================================
# import all handlers for the mud's urls
#==============================================================================

from mud.handlers.main      import      MainHandler
from mud.handlers.about     import     AboutHandler
from mud.handlers.login     import     LoginHandler
from mud.handlers.logout    import    LogoutHandler
from mud.handlers.register  import  RegisterHandler
from mud.handlers.websocket import WebSocketHandler

#==============================================================================
# start the server
#==============================================================================

define("port", default=9999, help="run on the given port", type=int)

def main():
    parse_command_line()
    app = tornado.web.Application(
        [
            (r"/"          ,      MainHandler),
            (r"/about"     ,     AboutHandler),
            (r"/login"     ,     LoginHandler),
            (r"/logout"    ,    LogoutHandler),
            (r"/register"  ,  RegisterHandler),
            (r"/websocket" , WebSocketHandler),
        ],
        cookie_secret = "secret2", #str(uuid.uuid4()),
        login_url     = "/login",
        template_path = os.path.join(ROOTDIR, "templates"),
        static_path   = os.path.join(ROOTDIR, "static"),
        xsrf_cookies  = True,
        debug         = DEBUG,
        autoreload    = False,
    )
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
