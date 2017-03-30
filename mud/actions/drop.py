# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .action import Action2, Action3
from mud.events import DropEvent, DropInEvent

class DropAction(Action2):
    EVENT = DropEvent
    RESOLVE_OBJECT = "resolve_for_use"
    ACTION = "drop"

class DropInAction(Action3):
    EVENT = DropInEvent
    RESOLVE_OBJECT = "resolve_for_use"
    RESOLVE_OBJECT2 = "resolve_for_operate"
    ACTION = "drop-in"
