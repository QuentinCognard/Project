# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .event import Event2

class InspectEvent(Event2):
    NAME = "look"

    def get_event_templates(self):
        return self.object.get_event_templates()

    def perform(self):
        if not self.actor.can_see():
            return self.failed_cannot_see()
        self.buffer_clear()
        self.buffer_inform("look.actor", object=self.object)
        if not self.object.is_container() or self.object.has_prop("closed"):
            return self.actor.send_result(self.buffer_get())
        players = []
        objects = []
        for x in self.object.contents():
            if x is self.actor:
                pass
            elif x.is_player():
                players.append(x)
            else:
                objects.append(x)
        if players or objects:
            self.buffer_inform("look.inside.intro")
            self.buffer_append("<ul>")
            for x in players:
                self.buffer_peek(x)
            for x in objects:
                self.buffer_peek(x)
            self.buffer_append("</ul>")
        else:
            self.buffer_inform("look.inside.empty")
        self.actor.send_result(self.buffer_get())

    def failed_cannot_see(self):
        self.fail()
        self.buffer_clear()
        self.buffer_inform("look.failed")
        self.actor.send_result(self.buffer_get())
