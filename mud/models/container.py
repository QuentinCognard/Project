# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .thing             import Thing
from .mixins.located    import Located
from .mixins.containing import Containing

class Container(Containing, Thing):

    """a Container contains objects and/or players.  For example: a box."""

    #--------------------------------------------------------------------------
    # initialization
    #--------------------------------------------------------------------------

    def __init__(self, **kargs):
        super().__init__(**kargs)

    def init_from_yaml(self, data, world):
        super().init_from_yaml(data, world)

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

    def is_container(self):
        return True

    def all(self):
        """return an iterator over all objects in/at the container."""
        yield from self.contents()
        yield from self.parts()

    def find_containing(self):
        return self
