# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .propertied import Propertied
import mud.game

class Containing(Propertied):

    """a mixin that provides the ability to have content."""

    #--------------------------------------------------------------------------
    # initialization
    #--------------------------------------------------------------------------

    def __init__(self, **kargs):
        super().__init__(**kargs)
        self._contents = set()

    #--------------------------------------------------------------------------
    # initialization from YAML data
    #--------------------------------------------------------------------------

    def init_from_yaml(self, data, world):
        super().init_from_yaml(data, world)
        self._contents = set()
        for i in data.get("contains", ()):
            mud.game.GAME.world[i].move_to(self)

    def update_from_yaml(self, data, world):
        super().update_from_yaml(data, world)

    #--------------------------------------------------------------------------
    # API for saving the dynamic part of objects to YAML (via JSON)
    #--------------------------------------------------------------------------

    def archive_into(self, obj):
        super().archive_into(obj)

    #--------------------------------------------------------------------------
    # contents API
    #--------------------------------------------------------------------------

    def contents(self):
        """return an iterator over the contents of the container."""
        return iter(self._contents)

    def __contains__(self, x):
        return x in self._contents

    def is_empty(self):
        return not self._contents

    def add(self, obj):
        """add an object or player to the container."""
        self._contents.add(obj)

    def remove(self, obj):
        """remove an object or player from the container."""
        self._contents.remove(obj)

    def reset(self):
        self._contents.clear()
        super().reset()
