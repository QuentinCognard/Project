# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

import mud.game
from .thing             import Thing
from .mixins.containing import Containing
from .location          import Location
import queue
from tornado.ioloop     import IOLoop

class Player(Containing, Thing):

    def __new__(cls, name=None, **kargs):
        player = mud.game.GAME.players.get(name, None)
        if player is not None:
            return player
        return super(Player, cls).__new__(cls)

    #--------------------------------------------------------------------------
    # initialization
    #--------------------------------------------------------------------------

    def __init__(self, name=None, **kargs):
        if hasattr(self, "name"):     # check if the player has already been initialized
            return                    # in which case, nothing more needs to be done
        kargs["id"] = pid = "player__" + name
        super().__init__(**kargs)     # otherwise, initialize base classes
        GAME = mud.game.GAME
        GAME.players[name] = self                       # save player in game dict
        self.transcript = GAME.transcripts.lookup(name) # and add appropriate attributes
        self.name = name
        self.yaml = {"id": pid, "name": name}
        user = mud.game.GAME.users[name]
        self.gender = user["gender"]
        self.description = user["description"]

    #--------------------------------------------------------------------------
    # initialization from YAML data
    #--------------------------------------------------------------------------

    def init_from_yaml(self, data, world):
        super().init_from_yaml(data, world)
        self.add_name(self.name)

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

    def is_player(self):
        return True

    def __str__(self):
        return self.name

    def can_see(self):
        if not self.container().has_prop("dark"):
            return True
        if self.has_prop("power-to-see-in-the-dark"):
            return True
        if self.find_for_light(prop="light-on"):
            return True
        return False

    def _has_prop_can_see(self):
        return self.can_see()

    def all(self):
        yield from self.contents()
        yield from self.parts()

    def is_alive(self):
        return bool(self.container())

    def noun_the(self):
        return self.name

    def noun_a(self):
        return self.name

    #--------------------------------------------------------------------------
    # API for sending messages back to the user through his websocket
    #--------------------------------------------------------------------------

    def _send(self, msg):
        ws = getattr(self, "websocket", None)
        if ws:
            IOLoop.current().add_callback(ws.write_message, msg)
            if msg["type"] != "death":
                self.transcript.append(msg)

    def send_echo(self, html):
        """sends back the commands as received."""
        self._send({"type": "echo", "html": html})

    def send_error(self, html):
        """sends an error message for a command that was not understood
        or could not be executed."""
        self._send({"type": "error", "html": html})

    def send_result(self, html):
        """sends a description that is a consequence from the user's last
        action."""
        self._send({"type": "result", "html": html})

    def send_info(self, html):
        """sends a description for an event not initiated by the user.
        for example, for actions of players in the same location."""
        self._send({"type": "info", "html": html})

    def reset(self):
        from mud.events import ResetEvent
        super().reset()
        ResetEvent(self).execute()

    #--------------------------------------------------------------------------
    # find API
    # when the player issues an order, this order will refer to objects by name
    # or make assumptions about the existence of objects with a certain
    # property, etc...  The MUD engine needs to find such objects that are
    # implicitly refered to.  However, different actions will use different
    # strategies (look in different places) to find such objects.  Below are
    # functions for performing the search in different use cases.
    #--------------------------------------------------------------------------

    def _make_find_pred(self, kargs):
        """create a function to test whether an object matches the given
        criteria."""
        test = kargs.get("test")          # a function           (optional)
        name = kargs.get("name")          # a name               (optional)
        prop = kargs.get("prop")          # a property           (optional)
        props= kargs.get("props")         # a list of properties (optional)
        def pred(x):                      # the new testing predicate
            return (((not test)  or text(x))          and
                    ((not name)  or x.has_name(name)) and
                    ((not prop)  or x.has_prop(prop)) and
                    ((not props) or x.has_props(props)))
        return pred

    def find_for_use(self, **kargs):
        """find an object that you can use/drop:
        - in your inventory"""
        pred = self._make_find_pred(kargs)
        for x in self.all():
            if pred(x):
                return x
        return None

    def find_for_operate(self, **kargs):
        """find an object that you can operate on:
        - in your inventory
        - in your immediate surroundings"""
        pred = self._make_find_pred(kargs)
        for x in self.all():
            if pred(x):
                return x
        c = self.container()
        parts = []
        if c is not None:
            for x in c.all():
                if pred(x):
                    return x
                parts.append(x)
        while parts:
            l = parts
            parts = []
            for x in l:
                for y in x.parts():
                    if pred(y):
                        return y
                    parts.append(y)
        return None

    def find_for_take(self, **kargs):
        """find an object that you can take:
        - in your surroundings
        - recursively inside open containers of your surroundings"""
        pred = self._make_find_pred(kargs)
        cont = self.container()
        if cont is None:
            return None
        q = queue.Queue()
        q.put(cont)
        while not q.empty():
            cont = q.get()
            for x in cont.all():
                if pred(x):
                    return x
                elif x is self:
                    q.put(x)
                elif isinstance(x, Containing) and \
                     not isinstance(x, Player) and \
                     not x.has_prop("closed"):
                    q.put(x)
        return None

    def find_for_light(self, **kargs):
        """find an object that can light your surroundings:
        - in your inventory
        - in your surroundings
        - or recursively in outer containers (unless you find that's
          closed and you can't look outside any further
        - or carried by people in your surroundings
        - or recursively by people in outer containers (that you
          can reach)"""
        pred = self._make_find_pred(kargs)
        for x in self.contents():
            if pred(x):
                return x
        q = queue.Queue()
        c = self.container()
        while c:
            q.put(c)
            c = c.is_container() and c.container()
        while not q.empty():
            c = q.get()
            for x in c.all():
                if pred(x):
                    return x
                if isinstance(x, Player):
                    for y in x.all():
                        if pred(y):
                            return y
        return None

    def find_for_go(self, **kargs):
        """find an exit in your surroundings."""
        c = self.container()
        if not c or not isinstance(c, Location):
            return None
        pred = self._make_find_pred(kargs)
        for x in c.exits():
            if pred(x):
                return x

    def resolve_for_use(self, **kargs):
        return self.find_for_use(**kargs)

    def resolve_for_operate(self, **kargs):
        if self.can_see():
            return self.find_for_operate(**kargs)
        else:
            return self.find_for_use(**kargs)

    def resolve_for_take(self, **kargs):
        if self.can_see():
            return self.find_for_take(**kargs)
        else:
            return None

    def resolve_for_go(self, **kargs):
        if self.can_see():
            return self.find_for_go(**kargs)
        else:
            return None
