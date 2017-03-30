# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .model import Model

class Portal(Model):

    """a Portal has 1 or more exits.  It mediates the traversal from one
    exit to another.  It can also hold properties shared with its exits."""

    #--------------------------------------------------------------------------
    # initialization
    #--------------------------------------------------------------------------

    def __init__(self, **kargs):
        super().__init__(**kargs)
        self.exits = []

    #--------------------------------------------------------------------------
    # initialization from YAML data
    #--------------------------------------------------------------------------

    def init_from_yaml(self, data, world):
        super().init_from_yaml(data, world)
        shared = data.get("shared-props")
        if shared is not None:
            if isinstance(shared, str):
                shared = [shared]
            assert all(isinstance(x,str) for x in shared)
        self.shared_props = shared
        for edata in data["exits"]:
            if "type" not in edata:
                edata["type"] = "Exit"
            obj = world.make(edata)
            obj.portal = self
            self.exits.append(obj)
            world.autocreated.append(obj)

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

    def other_exit(self, exit):
        # by default, pick the first other one
        for x in self.exits:
            if x is not exit:
                return x

    def get_traversal(self, exit):
        return PortalTraversal(exit, exit.other_exit())

    def commit_traversal(self, traversal):
        pass


class PortalTraversal:

    def __init__(self, exit1, exit2, commit=None):
        self.exit1 = exit1
        self.exit2 = exit2
        self._commit = commit
        self.portal = exit1.portal

    def commit(self):
        if self._commit:
            self._commit()
        else:
            self.portal.commit_traversal(self)
