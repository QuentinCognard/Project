# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .event import Event2, Event3

class OpenEvent(Event2):
    NAME = "open"

    def perform(self):
        self.inform("open")


class OpenWithEvent(Event3):
    NAME = "open-with"

    def perform(self):
        self.inform("open-with")
