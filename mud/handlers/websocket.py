# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from mud.handlers.base import BaseHandler
import mud.game

import tornado.websocket
import tornado.escape
import threading

#==============================================================================
# handler for ajax submission of user commands
#==============================================================================

class WebSocketHandler(BaseHandler, tornado.websocket.WebSocketHandler):
    opensockets = set()
    lock = threading.RLock()

    def open(self):
        user = self.get_secure_cookie("mud_player")
        if not user:
            self.close()
            return
        self.player = self.get_player()
        self.player.websocket = self      # the player knows its websocket
        self.opensockets.add(self)
        mud.game.GAME.engine.put({"type":"birth", "player":self.player})

    def on_close(self):
        del self.player.websocket         # remove websocket from player
        self.opensockets.remove(self)

    def on_message(self, message):
        msg = tornado.escape.json_decode(message)
        msg["player"] = self.player       # add player to received message
        mud.game.GAME.engine.put(msg)
