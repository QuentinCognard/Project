# -*- coding: utf-8 -*-
#==============================================================================

from .effect import Effect2
from mud.events import ShootEvent

class ShootEffect(Effect2):
    EVENT = ShootEvent
