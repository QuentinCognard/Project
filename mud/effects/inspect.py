# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .effect import Effect2
from mud.events import InspectEvent

class InspectEffect(Effect2):
    EVENT = InspectEvent
