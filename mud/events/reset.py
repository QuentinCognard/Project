# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .event import Event1

class ResetEvent(Event1):
    NAME = "reset"

    def perform(self):
        self.inform("reset")
