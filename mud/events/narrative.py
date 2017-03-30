# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .event import Event1

class NarrativeEvent(Event1):
    NAME = "narrative"

    @property
    def at(self):
        return self.actor

    def get_event_templates(self):
        return self.at.get_event_templates()

    def perform(self):
        key = self.key
        for observer in self.observers():
            self.buffer_clear()
            self.buffer_inform(key+".observer", observer=observer)
            html = self.buffer_get()
            if html:
                getattr(observer, self.SEND_OBSERVER)(html)

    def observers(self):
        cont = self.at.find_containing()
        stack = [cont]
        while stack:
            cont = stack.pop()
            for x in cont.contents():
                if x.is_player() and x.can_see():
                    yield x
            if cont.is_container() and not cont.has_prop("closed"):
                cont = cont.container()
                if cont:
                    stack.append(cont)
