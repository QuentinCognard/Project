# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .effect import Effect1
from mud.events import NarrativeEvent

class NarrativeEffect(Effect1):
    EVENT = NarrativeEvent

    def resolve_actor(self):
        return self.resolve("at")

    def make_event(self):
        e = super().make_event()
        e.key = self.yaml["key"]
        return e
