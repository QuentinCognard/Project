# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

import tornado.escape

class BaseHandler(tornado.web.RequestHandler):

    # all handlers need to identify the current player

    def get_current_user(self):
        player_json = self.get_secure_cookie("mud_player")
        if not player_json: return None
        return tornado.escape.json_decode(player_json)

    def get_player(self):
        username = self.get_current_user()
        if username is None:
            return None
        import mud.models.player
        return mud.models.player.Player(username)
