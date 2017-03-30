# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .identified import Identified

class Located(Identified):

    """mixin class that provides the ability to be located in the world, i.e.
    to be stored in a Containing model which could be a location in the world,
    or something like a box, or a player's inventory."""

    #--------------------------------------------------------------------------
    # initialization
    #--------------------------------------------------------------------------
    
    def __init__(self, **kargs):
        super().__init__(**kargs)
        self._container = None

    #--------------------------------------------------------------------------
    # initialization from YAML data
    #--------------------------------------------------------------------------

    def init_from_yaml(self, data, world):
        super().init_from_yaml(data, world)
        if "container" in data:
            self.move_to(world[data["container"]])

    def update_from_yaml(self, data, world):
        super().update_from_yaml(data, world)
        if "container" in data:
            loc = data["container"]
            self.move_to(loc and world[loc])

    #--------------------------------------------------------------------------
    # API for saving the dynamic part of objects to YAML (via JSON)
    #--------------------------------------------------------------------------

    def archive_into(self, obj):
        super().archive_into(obj)
        if self._container:
            obj["container"] = self._container.id
        else:
            obj["container"] = None

    #--------------------------------------------------------------------------
    # model API
    #--------------------------------------------------------------------------

    def move_to(self, cont):
        """remove the object from its current Containing model and add it to
        another Containing model, thus performing a move operation."""
        if self._container:
            self._container.remove(self)
            self._container = None
        if cont:
            cont.add(self)
            self._container = cont

    def container(self):
        return self._container

    def reset(self):
        self._container = None
        super().reset()

    def find_containing(self):
        if self._container:
            return self._container.find_containing()
        if hasattr(self, "part_of"):
            return self.part_of.find_containing()
