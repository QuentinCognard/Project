# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .action import Action2
from mud.events import LightOnEvent, LightOffEvent

class LightOnAction(Action2):
    EVENT = LightOnEvent
    ACTION = "light-on"
    RESOLVE_OBJECT = "resolve_for_use"

class LightOffAction(Action2):
    EVENT = LightOffEvent
    ACTION = "light-off"
    RESOLVE_OBJECT = "resolve_for_use"
