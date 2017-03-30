# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .event import Event1

class FailedActionEvent(Event1):
    NAME = "failed-action"

    def __init__(self, actor, action):
        super().__init__(actor)
        self.action = action

    def context(self):
        context = super().context()
        context["action"] = self.action
        return context

    def perform(self):
        self.inform("failed-action")
