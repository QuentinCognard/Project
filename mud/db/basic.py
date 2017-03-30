# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

import threading, os, os.path, json, pickle

#==============================================================================
# basic functionality for all databases
#==============================================================================

class BasicDB(dict):

    def __init__(self, filename):
        self.lock = threading.RLock()
        self.json_path = "%s.json" % filename
        self.pickle_path = "%s.pckl" % filename

    def reset(self):
        self.clear()

    def json_save(self):
        with self.lock:
            os.makedirs(os.path.dirname(self.json_path), exist_ok=True)
            with open(self.json_path, "w") as f:
                json.dump(self, f, ensure_ascii=False, indent=4)

    def json_load(self, required=False):
        try:
            with open(self.json_path, "r") as f:
                data = json.load(f)
            with self.lock:
                self.clear()
                self.update(data)
        except FileNotFoundError:
            if required:
                raise

    def pickle_save(self):
        with self.lock:
            os.makedirs(os.path.dirname(self.pickle_path), exist_ok=True)
            with open(self.pickle_path, "wb") as f:
                pickle.dump(dict(self), f, protocol=-1)

    def pickle_load(self, required=False):
        try:
            with open(self.pickle_path, "rb") as f:
                data = pickle.load(f)
            with self.lock:
                self.clear()
                self.update(data)
        except FileNotFoundError:
            if required:
                raise
        except EOFError:
            if required:
                raise

    save = pickle_save
    load = pickle_load
