# -*- coding: utf-8 -*-
#==============================================================================

from .event import Event3

class ShootEvent(Event3):
    NAME = "shoot"

    def perform(self):
        if not self.object.has_prop("shootable"):
            return self.shoot_failed()
        if not self.object2.has_prop("gun"):
            return self.shoot_failed()
        self.object.move_to(None)
        self.object2.move_to(None)
        self.inform("shoot")

    def shoot_failed(self):
        self.fail()
        self.inform("shoot.failed")
