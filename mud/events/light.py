# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .event import Event2

class LightOnEvent(Event2):
    NAME = "light-on"

    def perform(self):
        if not self.object.has_prop("lightable"):
            self.fail()
            return self.inform("light-on.failed")
        self.inform("light-on")


class LightOffEvent(Event2):
    NAME = "light-off"

    def perform(self):
        if not self.object.has_prop("lightable"):
            self.fail()
            return self.inform("light-off.failed")
        self.inform("light-off")
