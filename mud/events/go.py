# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .event import Event2
from .info  import InfoEvent


class EnterPortalEvent(Event2):
    NAME = "enter-portal"

    @property
    def exit(self):
        return self.object

    def perform(self):
        if self.get_datum("enter-portal.data-driven"):
            return self.perform_data_driven()
        self.traversal = self.exit.get_traversal()
        if self.actor.has_prop("power-to-pass"):
            # magical power to pass through portals
            # even when closed.
            pass
        elif self.traversal.exit1.has_prop("closed"):
            self.add_prop("cannot-pass")
            self.add_prop("cannot-pass-exit1")
            return self.enter_portal_failure()
        elif self.traversal.exit2.has_prop("closed"):
            self.add_prop("cannot-pass")
            self.add_prop("cannot-pass-exit2")
            return self.enter_portal_failure()
        elif self.traversal.portal.has_prop("closed"):
            self.add_prop("cannot-pass")
            self.add_prop("cannot-pass-portal")
            return self.enter_portal_failure()
        self.enter_portal_success()
        self.execute_effects()
        TraversePortalEvent(self.actor, self.traversal).execute()

    def enter_portal_success(self):
        self.inform("enter-portal")

    def enter_portal_failure(self):
        self.fail()
        self.inform("enter-portal.failed")

    def context(self):
        context = super().context()
        context["exit"] = self.exit
        context["portal"] = self.exit.portal
        return context

    def perform_data_driven(self):
        self.inform("enter-portal")
        # effects do the rest


class TraversePortalEvent(Event2):
    NAME = "traverse-portal"

    @property
    def traversal(self):
        return self.object

    def perform(self):
        self.inform("traverse-portal")
        self.traversal.commit()
        self.actor.move_to(self.traversal.exit2.location)
        self.execute_effects()
        LeavePortalEvent(self.actor, self.traversal.exit2).execute()

    def context(self):
        context = super().context()
        context["traversal"] = self.traversal
        context["exit1"]     = self.traversal.exit1
        context["exit2"]     = self.traversal.exit2
        context["portal"]    = self.traversal.portal
        return context

    def get_event_templates(self):
        return None


class LeavePortalEvent(Event2):
    NAME = "leave-portal"

    @property
    def exit(self):
        return self.object

    def perform(self):
        self.inform("leave-portal")
        InfoEvent(self.actor).execute()

    def context(self):
        context = super().context()
        context["exit"] = self.exit
        context["portal"] = self.exit.portal
        return context


class MoveEvent(Event2):
    NAME = "move"

    @property
    def exit(self):
        return self.object

    def perform(self):
        self.actor.move_to(self.object)
