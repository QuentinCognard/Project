# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .event import Event2

class ChangePropEvent(Event2):
    NAME = "change-prop"

    def get_event_templates(self):
        return self.object.get_event_templates()

    def perform(self):
        props = self.modifs
        if isinstance(props, str):
            props = [props]
        self.object.change_props(props, self.world_context())

    def __init__(self, actor, object, modifs):
        super().__init__(actor, object)
        self.modifs = modifs
