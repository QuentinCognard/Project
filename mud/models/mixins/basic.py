# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

class Basic:

    """primitive base class for all models and mixins."""

    #--------------------------------------------------------------------------
    # initialization
    #--------------------------------------------------------------------------

    def __init__(self, **kargs):
        pass

    #--------------------------------------------------------------------------
    # initialization from YAML data
    #--------------------------------------------------------------------------

    def init_from_yaml(self, data, world):
        pass

    def update_from_yaml(self, data, world):
        pass

    #--------------------------------------------------------------------------
    # API for saving the dynamic parts of objects to YAML (via JSON)
    #--------------------------------------------------------------------------

    def to_json(self):
        obj = {}
        self.archive_into(obj)
        return obj

    def archive_into(self, obj):
        pass

    #--------------------------------------------------------------------------
    # MUD API
    #--------------------------------------------------------------------------

    def reset(self):
        pass
