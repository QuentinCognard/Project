# -*- coding: utf-8 -*-
#==============================================================================

from .action import Action3
from mud.events import ShootEvent

class ShootAction(Action3):
    EVENT = ShootEvent
    RESOLVE_OBJECT = "resolve_for_operate"
    RESOLVE_OBJECT2 = "resolve_for_use"
    ACTION = "shoot"
