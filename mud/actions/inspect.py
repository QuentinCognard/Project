# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .action import Action2
from mud.events import InspectEvent

class InspectAction(Action2):
    EVENT = InspectEvent
    RESOLVE_OBJECT = "resolve_for_take"
    ACTION = "inspect"
