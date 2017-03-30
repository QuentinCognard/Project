# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

import tornado.ioloop
import threading, queue
import mud.parser
import mud.game

class Engine(threading.Thread):

    def __init__(self):
        super().__init__(daemon=True)
        self._queue = queue.Queue()
        self.put = self._queue.put
        self.again = True
        rules = mud.game.GAME.module.make_rules()
        self.parser = mud.parser.Parser(rules)

    def run(self):
        while self.again:
            task = self._queue.get()
            self.perform(task)

    def perform(self, task):
        meth = "perform_%s" % task["type"]
        meth = getattr(self, meth)
        meth(task)

    def perform_input(self, task):
        actor = task["player"]
        text  = task["text"].strip()
        actor.send_echo("<pre>%s</pre>" % text)
        if actor.is_alive():
            action,text = self.parser.parse(actor, text)
        else:
            from mud.events import DeadAction
            # this is actually an event, but it also has an execute method
            action = DeadAction(actor)
        if action:
            action.execute()
        else:
            actor.send_error("<p>hein?</p>")

    def perform_save(self, task):
        actor = task["player"]
        mud.game.GAME.save()
        actor.send_info("<p>Sauvegarde effectuée!</p>")

    def perform_birth(self, task):
        actor = task["player"]
        if not actor.container():
            from mud.events.birth import BirthEvent
            BirthEvent(actor).execute()

    def perform_reset(self, task):
        actor = task["player"]
        mud.game.GAME.reset()
