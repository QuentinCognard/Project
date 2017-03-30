# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .event import Event1

class DeathEvent(Event1):
    NAME = "death"

    def perform(self):
        self.inform("death")
        cont = self.actor.container()
        for x in list(self.actor.contents()):
            x.move_to(cont)
        self.actor.move_to(None)
