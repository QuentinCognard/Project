# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from mud.db.basic import BasicDB

class TranscriptDB(BasicDB):

    def lookup(self, username):
        with self.lock:
            trans = self.get(username, None)
            if trans is None:
                trans = []
                self[username] = trans
            return trans

    def reset_players(self):
        for t in self.values():
            t.clear()
