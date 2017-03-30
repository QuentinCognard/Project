# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from mud.handlers.base import BaseHandler

#==============================================================================
# about page
#==============================================================================

class AboutHandler(BaseHandler):

    def get(self):
        self.render("about.html")
