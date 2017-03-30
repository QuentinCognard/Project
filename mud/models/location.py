# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

import re
from .model import Model
from .mixins.containing import Containing

class Location(Containing, Model):

    """a Location contains stuff and has exits; but it is not itself located in
    something else."""

    #--------------------------------------------------------------------------
    # initialization
    #--------------------------------------------------------------------------

    def __init__(self, **kargs):
        super().__init__(**kargs)
        self._exits = [] # through these exits, portals can be traversed to other locations

    #--------------------------------------------------------------------------
    # initialization from YAML data
    #--------------------------------------------------------------------------

    def init_from_yaml(self, data, world):
        super().init_from_yaml(data, world)
        if "portals" in data:
            self.portals = [world[id] for id in data["portals"]]

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

    def is_location(self):
        return True

    def add_exit(self, e):
        self._exits.append(e)

    def find_exit(self, direction):
        for e in self._exits:
            if e.direction == direction:
                return e

    def exits(self):
        return iter(self._exits)

    def all(self):
        yield from self.contents()
        yield from self.parts()
        yield from self.exits()

    def find_containing(self):
        return self
