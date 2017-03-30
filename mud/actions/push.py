# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .action import Action2
from mud.events import PushEvent

class PushAction(Action2):
    EVENT = PushEvent
    RESOLVE_OBJECT = "resolve_for_operate"
    ACTION = "push"
