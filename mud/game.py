# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

import os, os.path, yaml, glob
import mud.server
from mud.engine                import Engine
from mud.world                 import World
from mud.db.transcript         import TranscriptDB
from mud.db.user               import UserDB
from mud.models.mixins.evented import Evented

class Game:

    GAMES_DIR = os.path.join(os.path.dirname(__file__), "games")
    SAVES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".games")

    def yaml_initial_glob(self):
        return os.path.join(self.GAMES_DIR, self.name, "*initial*.yml")

    def yaml_static_glob(self):
        return os.path.join(self.GAMES_DIR, self.name, "*static*.yml")

    def yaml_current_filename(self):
        return os.path.join(self.SAVES_DIR, self.name, "current.yml")

    def transcripts_filename(self):
        return os.path.join(self.SAVES_DIR, self.name, "transcripts")

    def users_filename(self):
        return os.path.join(self.SAVES_DIR, self.name, "users")

    def __init__(self, name=None, initial=None, current=None, static=None):
        self._for_reset  = {"name"   : name   ,
                            "initial": initial,
                            "current": current,
                            "static" : static }
        self.name        = name
        self.world       = World()
        self.static      = {}
        self.transcripts = TranscriptDB(self.transcripts_filename())
        self.users       = UserDB(self.users_filename())
        self.players     = {}
        self.engine      = None
        self._initial    = initial
        self._current    = current
        self._static     = static
        if initial is None:
            self._initial = self.yaml_load_all_glob(self.yaml_initial_glob())
        if current is None:
            self._current = self.yaml_load_all(self.yaml_current_filename())
        if static  is None:
            self._static = self.yaml_load_glob(self.yaml_static_glob())

    def yaml_load_all_glob(self, pattern):
        l = []
        for filename in glob.glob(pattern):
            l.extend(self.yaml_load_all(filename))
        return l

    def yaml_load_all(self, filename):
        try:
            return list(yaml.load_all(open(filename)))
        except FileNotFoundError:
            return []

    def yaml_load(self, filename):
        try:
            return yaml.load(open(filename))
        except FileNotFoundError:
            return {}

    def yaml_load_glob(self, pattern):
        d = {}
        for filename in glob.glob(pattern):
            d.update(self.yaml_load(filename))
        return d

    def game_module_load(self):
        import importlib
        self.module = importlib.import_module("mud.games.%s" % self.name)
    
    def load(self):
        self.game_module_load()
        self.users.load()
        self.transcripts.load()
        self.static.update(self._static)
        self.users.create_avatars()
        self.world.load(self._initial, self._current)
        del self._initial
        del self._current
        del self._static

    def save(self):
        contents = self.world.save()
        with open(self.yaml_current_filename(), "w") as stream:
            yaml.dump_all(contents, stream)
        self.transcripts.save()
        self.users.save()

    def start_for_player(self, player):
        init = self.static["start"]
        return self.world[init]

    def remove(self, filename):
        try:
            os.remove(filename)
        except FileNotFoundError:
            pass

    def remove_glob(self, filename):
        for path in glob.glob(filename):
            self.remove(path)

    def reset(self):
        self.users.reset_avatars()
        self.transcripts.reset_players()
        self.remove(self.yaml_current_filename())
        self.remove_glob(self.transcripts_filename() + ".*")
        self.__init__(**self._for_reset)
        self.load()

    def start(self):
        self.engine = Engine()
        self.engine.start()
        mud.server.main()
