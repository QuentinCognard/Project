# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .event import Event2
from .info  import InfoEvent
import mud.game

class TeleportEvent(Event2):
    NAME = "teleport"

    def perform(self):
        n = len(self.object)
        if n == 0:
            self.fail()
            self.inform("teleport.not-found")
        elif n > 1:
            self.fail()
            self.inform("teleport.ambiguous")
        else:
            self.inform("teleport.departure")
            self.actor.move_to(self.object[0])
            self.inform("teleport.arrival")
            InfoEvent(self.actor).execute()

    def get_event_templates(self):
        return self.actor.get_event_templates()
