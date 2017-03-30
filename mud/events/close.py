# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .event import Event2, Event3

class CloseEvent(Event2):
    NAME = "close"

    def perform(self):
        self.inform("close")


class CloseWithEvent(Event3):
    NAME = "close-with"

    def perform(self):
        self.inform("close-with")
