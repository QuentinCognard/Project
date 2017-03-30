# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .action import Action1
from mud.events import LookEvent

class LookAction(Action1):
    EVENT = LookEvent
    ACTION = "look"
