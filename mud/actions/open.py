# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .action import Action2, Action3
from mud.events import OpenEvent, OpenWithEvent


class OpenAction(Action2):
    EVENT = OpenEvent
    RESOLVE_OBJECT = "resolve_for_operate"
    ACTION = "open"


class OpenWithAction(Action3):
    EVENT = OpenWithEvent
    RESOLVE_OBJECT = "resolve_for_operate"
    RESOLVE_OBJECT2 = "resolve_for_use"
    ACTION = "open-with"
