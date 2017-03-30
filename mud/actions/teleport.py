# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .action                      import Action2
from mud.events                   import TeleportEvent
from mud.models.mixins.containing import Containing
from mud.models                   import Player
import mud.game

class TeleportAction(Action2):
    EVENT = TeleportEvent
    ACTION = "teleport"

    def resolve_object(self):
        world = mud.game.GAME.world
        loc = world.get(self.object)
        if loc:
            locs = [loc]
        else:
            locs = []
            for k,v in world.items():
                if isinstance(v, Containing) and \
                   not isinstance(v, Player) and \
                   k.find(self.object) != -1:
                    locs.append(v)
        return locs
