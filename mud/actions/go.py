# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .action import Action2
from mud.events import EnterPortalEvent
import mud.game

class GoAction(Action2):
    EVENT = EnterPortalEvent
    RESOLVE_OBJECT = "resolve_for_go"
    ACTION = "go"
    RESOLVE_MAP = {}

    def resolve_object(self):
        if not self.RESOLVE_MAP:
            STATIC = mud.game.GAME.static
            self.RESOLVE_MAP.update(STATIC["directions"]["normalized"])
            self.RESOLVE_MAP.update((v,k) for (k,v) in STATIC["directions"]["noun_the"].items())
            self.RESOLVE_MAP.update((v,k) for (k,v) in STATIC["directions"]["noun_at_the"].items())
        self.object = self.RESOLVE_MAP.get(self.object, None)
        return super().resolve_object()


class LeaveAction(Action2):
    EVENT = EnterPortalEvent
    ACTION = "leave"

    def __init__(self, subject):
        super().__init__(subject, None)

    def resolve_object(self):
        return self.subject.resolve_for_go(prop="for-leave")


class EnterAction(Action2):
    EVENT = EnterPortalEvent
    ACTION = "enter"

    def __init__(self, subject):
        super().__init__(subject, None)

    def resolve_object(self):
        return self.subject.resolve_for_go(prop="for-enter")
