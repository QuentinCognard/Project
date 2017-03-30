# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .action import Action3
from mud.events import TypeEvent

class TypeAction(Action3):
    EVENT = TypeEvent
    ACTION = "type"
    RESOLVE_OBJECT = "resolve_for_operate"

    def __init__(self, subject, object):
        super().__init__(subject, "ordinateur", object)

    def resolve_object2(self):
        return self.object2
