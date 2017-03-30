# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .event import Event2

class PushEvent(Event2):
    NAME = "push"

    def perform(self):
        if not self.object.has_prop("pushable"):
            self.fail()
            return self.inform("push.failed")
        self.inform("push")
