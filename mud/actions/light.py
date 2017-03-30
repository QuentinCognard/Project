# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .action import Action2
from .action import Action3
from mud.events import LightOnEvent, LightOffEvent, LightWithEvent

class LightOnAction(Action2):
    EVENT = LightOnEvent
    ACTION = "light-on"
    RESOLVE_OBJECT = "resolve_for_use"

class LightOffAction(Action2):
    EVENT = LightOffEvent
    ACTION = "light-off"
    RESOLVE_OBJECT = "resolve_for_use"

class LightWithAction(Action3):
    EVENT = LightWithEvent
    ACTION = "light-with"
    RESOLVE_OBJECT = "resolve_for_operate"
    RESOLVE_OBJECT2 = "resolve_for_use"
    