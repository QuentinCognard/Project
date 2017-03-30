# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .model import Model
import mud.game

class Exit(Model):

    """an Exit is available at a Location, in a certain direction.  It is
    connected to a Portal which itself is connected to 0 or more other exits."""

    _NEEDS_ID = False

    #--------------------------------------------------------------------------
    # initialization
    #--------------------------------------------------------------------------

    def __init__(self, **kargs):
        super().__init__(**kargs)
        self.portal      = None
        self.location    = None
        self.direction   = None

    #--------------------------------------------------------------------------
    # initialization from YAML data
    #--------------------------------------------------------------------------

    def init_from_yaml(self, data, world):
        super().init_from_yaml(data, world)
        self.location  = world[data["location"]]
        self.direction = data.get("direction")
        self.add_name(self.direction)
        self.location.add_exit(self)
        shared = data.get("shared-props")
        if shared is not None:
            if isinstance(shared, str):
                shared = [shared]
            assert all(isinstance(x,str) for x in shared)
        self.shared_props = shared

    def update_from_yaml(self, data, world):
        super().update_from_yaml(data, world)

    #--------------------------------------------------------------------------
    # API for saving the dynamic part of objects to YAML (via JSON)
    #--------------------------------------------------------------------------

    def archive_into(self, obj):
        super().archive_into(obj)

    #--------------------------------------------------------------------------
    # model API
    #--------------------------------------------------------------------------

    def is_exit(self):
        return True

    # in this design, all exits of the same portal share the same properties
    # which are stored on the portal
    #def props_proxy(self):
    #    return self.portal

    def prop_proxy(self, prop):
        if self.shared_props is not None:
            if prop in self.shared_props:
                return self.portal
            return self
        if self.portal.shared_props is not None:
            if prop in self.portal.shared_props:
                return self.portal
            return self
        shared = self.get_datum("shared-props", deref_last=False)
        if shared is not None:
            if isinstance(shared, str):
                shared = [shared]
            assert all(isinstance(x, str) for x in shared)
            self.shared_props = shared
            if prop in shared:
                return self.portal
        self.shared_props = []
        return self

    def other_exit(self):
        return self.portal.other_exit(self)

    def get_traversal(self):
        tr = self.get_datum("traversal", exit1=self, exit=self, portal=self.portal)
        if not tr:
            tr = self.portal.get_datum("traversal", exit1=self, exit=self, portal=self.portal)
        if not tr:
            return self.portal.get_traversal(self)
        from mud.effects.effect import Effect
        ctx = self.context()
        ctx["exit1"] = self
        ctx["portal"] = self.portal
        e = Effect(tr, ctx)
        exit1 = e.resolve("exit1")
        exit2 = e.resolve("exit2")
        from mud.models.portal import PortalTraversal
        return PortalTraversal(exit1, exit2)

    def the_direction(self):
        return mud.game.GAME.static["directions"]["noun_the"][self.direction]

    def find_containing(self):
        return self.location and self.location.find_containing()
