# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from mud.db.basic import BasicDB
import hashlib

class UserDB(BasicDB):

    # created using uuidgen
    SEED = b"77837fb0-69af-4f2c-8fbf-096e50d253c6"

    def authenticate(self, username, password):
        with self.lock:
            msg = hashlib.sha256()
            msg.update(self.SEED)
            msg.update(password.encode())
            password = msg.hexdigest()
            user = self.get(username, None)
            return user and user["password"]==password

    def create_user(self, username, password, description, gender):
        with self.lock:
            if username in self:
                return None
            msg = hashlib.sha256()
            msg.update(self.SEED)
            msg.update(password.encode())
            password = msg.hexdigest()
            user = {
                "username"   : username,
                "password"   : password,
                "description": description,
                "gender"     : gender
            }
            self[username] = user
            self.save()
            return user

    def create_avatars(self):
        from mud.models.player import Player
        with self.lock:
            for username in self:
                Player(username)

    def reset_avatars(self):
        from mud.models.player import Player
        with self.lock:
            for username in self:
                Player(username).reset()
