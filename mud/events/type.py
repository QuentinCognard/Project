# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .event import Event3

class TypeEvent(Event3):
    NAME = "type"

    def perform(self):
        self.add_prop("typed-"+self.object2)
        self.inform("type")
