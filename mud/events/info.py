# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .event import Event1


class InfoEvent(Event1):
    NAME = "info"
    SEND_ACTOR = "send_info"

    def get_event_templates(self):
        return self.actor.container().get_event_templates()

    def context(self):
        context = super().context()
        if "peeked" not in context:
            context["peeked"] = self.actor
        return context

    def perform(self):
        self.inform("info")
