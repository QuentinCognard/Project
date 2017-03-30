# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .effect import Effect2, Effect3
from mud.events import LightOnEvent, LightOffEvent

class LightOnEffect(Effect2):
    EVENT = LightOnEvent

class LightOffEffect(Effect3):
    EVENT = LightOffEvent
