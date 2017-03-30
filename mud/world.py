# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

import os.path

class World:

    def __init__(self):
        self.database = {}
        self.types    = {}

    def load_models(self):
        import mud.models as models
        Model = models.Model
        for k,v in models.__dict__.items():
            if not k.startswith("_") and type(v) is type and issubclass(v, Model):
                self.types[v.__name__] = v

    def make(self, data):
        if data is None:
            return None
        cls = self.types[data["type"]]
        obj = cls(**data)                 # autoadded to database
        obj.yaml = data
        if "id" not in data:
            data["id"] = obj.id
        return obj

    def load(self, initial, current):
        from yaml import load_all

        self.load_models()
        self.autocreated = []

        # create all objects in the world (except players)
        contents = initial
        for data in contents:
            obj = self.make(data)

        # initialize them with the initial yaml data
        for obj in tuple(self.database.values()):
            obj.init_from_yaml(obj.yaml, self)

        # initialize autocreated objects with their yaml data
        while self.autocreated:
            objs = self.autocreated
            self.autocreated = []
            for obj in objs:
                obj.init_from_yaml(obj.yaml, self)

        # update them with the saved current state of the game
        for data in current:
            key = data["id"]
            obj = self.database[key]
            obj.update_from_yaml(data, self)

    def save(self):
        return [x.to_json() for x in self.database.values()]

    def __getitem__(self, id):
        return self.database[id]

    def __setitem__(self, id, val):
        if id in self.database:
            raise Exception("id collision: %s" % id)
        self.database[id] = val

    def get(self, key, default=None):
        return self.database.get(key, default)

    def keys(self):
        return self.database.keys()

    def values(self):
        return self.database.values()

    def items(self):
        return self.database.items()
