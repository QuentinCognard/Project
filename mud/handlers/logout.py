# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from mud.handlers.base import BaseHandler

#==============================================================================
# log out handler
#==============================================================================

class LogoutHandler(BaseHandler):

    def get(self):
        self.clear_cookie("mud_player")
        self.redirect("/login")
