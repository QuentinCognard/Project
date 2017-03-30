# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .event import Event1

class DeadAction(Event1):
    NAME = "dead-action"

    def perform(self):
        self.inform("dead-action")
