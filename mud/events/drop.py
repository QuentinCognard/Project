# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .event import Event2, Event3


class DropEvent(Event2):
    NAME = "drop"

    def perform(self):
        self.object.move_to(self.actor.container())
        self.inform("drop")


class DropInEvent(Event3):
    NAME = "drop-in"

    def perform(self):
        if not self.object2.is_container():
            self.add_prop("object2-not-container")
            return self.drop_in_failure()
        if self.object not in self.actor:
            self.add_prop("object-not-in-inventory")
            return self.drop_in_failure()
        if not self.get_datum("drop-in.data-driven"):
            self.object.move_to(self.object2)
        self.inform("drop-in")

    def drop_in_failure(self):
        self.fail()
        self.inform("drop-in.failed")
