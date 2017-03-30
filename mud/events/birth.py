# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .event import Event1
from .info  import InfoEvent

class BirthEvent(Event1):
    NAME = "birth"

    def perform(self):
        from mud.game import GAME
        loc = GAME.start_for_player(self.actor)
        self.actor.move_to(loc)
        self.inform("birth")
        InfoEvent(self.actor).execute()
