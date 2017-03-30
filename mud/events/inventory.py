# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .event import Event1

class InventoryEvent(Event1):
    NAME = "inventory"

    def perform(self):
        self.buffer_clear()
        if self.actor.is_empty():
            self.buffer_inform("inventory.empty")
        else:
            self.buffer_inform("inventory.intro")
            self.buffer_append("<ul>")
            for x in self.actor.contents():
                self.buffer_peek(x)
            self.buffer_append("</ul>")
        self.actor.send_result(self.buffer_get())
