# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .action import Action2
from mud.events import CloseEvent

class CloseAction(Action2):
    EVENT = CloseEvent
    RESOLVE_OBJECT = "resolve_for_operate"
    ACTION = "close"
