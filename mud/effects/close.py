# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .effect import Effect2, Effect3
from mud.events import CloseEvent, CloseWithEvent

class CloseEffect(Effect2):
    EVENT = CloseEvent


class CloseWithEffect(Effect3):
    EVENT = CloseWithEvent
