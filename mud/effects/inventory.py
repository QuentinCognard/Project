# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .effect import Effect1
from mud.events import InventoryEvent

class InventoryEffect(Effect1):
    EVENT = InventoryEvent
