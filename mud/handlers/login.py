# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

import tornado.escape
from mud.handlers.base import BaseHandler
import mud.game

#==============================================================================
# the login handler uses the user database
#==============================================================================

class LoginHandler(BaseHandler):

    def extras(self):
        return {
            "next"        : self.get_argument("next", "/"),
            "login_error" : False,
        }

    def get(self):
        self.render("login.html", **self.extras())

    def post(self):
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")
        extras = self.extras()
        auth = mud.game.GAME.users.authenticate(username, password)
        if auth:
            self.set_secure_cookie("mud_player",
                                   tornado.escape.json_encode(username))
            self.redirect(extras["next"])
        else:
            extras["login_error"] = True
            self.clear_cookie("mud_player")
            self.render("login.html", **extras)
