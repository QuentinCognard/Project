# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .effect import Effect2
from mud.events import EnterPortalEvent, TraversePortalEvent, LeavePortalEvent, MoveEvent
from mud.models.portal import PortalTraversal


class EnterPortalEffect(Effect2):
    EVENT = EnterPortalEvent

    def resolve_object(self):
        return self.resolve("exit")


class TraversePortalEffect(Effect2):
    EVENT = TraversePortalEvent

    def resolve_object(self):
        exit1 = self.resolve("exit1")
        exit2 = self.resolve("exit2")
        return PortalTraversal(exit1, exit2)


class LeavePortalEffect(Effect2):
    EVENT = LeavePortalEvent

    def resolve_object(self):
        return self.resolve("exit")


class MoveEffect(Effect2):
    EVENT = MoveEvent

    def resolve_object(self):
        return self.resolve("to")
