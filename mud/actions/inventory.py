# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .action import Action1
from mud.events import InventoryEvent

class InventoryAction(Action1):
    EVENT = InventoryEvent
    ACTION = "inventory"
