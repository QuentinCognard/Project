# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from tornado.template import Template
from mud.models.mixins.evented import Evented
from mud.models.mixins.propertied import Propertied
from mud.models.mixins.containing import Containing
import re

class Event(Evented, Propertied):

    NAME = None
    SEND_ACTOR = "send_result"
    SEND_OBSERVER = "send_info"

    def __init__(self):
        super().__init__()
        self._effects_executed = False
        self._failed = False

    def execute(self):
        self.perform()
        self.execute_effects()

    def perform(self):
        raise NotImplemented()

    def execute_effects(self):
        if not self._effects_executed and not self._failed:
            self._effects_executed = True
            for effect in self.get_effects(self.NAME):
                effect.execute()

    def fail(self):
        self._failed = True

    def format(self, template, **kargs):
        context = self.context()
        context.update(kargs)
        return Template(template).generate(**context).decode()

    def to_html(self, text):
        text = text.strip()
        if not text or text[0]=="<":
            return text
        text = re.sub(r"(?:(?:^|\n)\s*){2,}", r"\n\n", text)
        html = ["<p>%s</p>" % s for s in text.split(r"\n\n")]
        return "\n".join(html)

    def buffer_clear(self):
        self.HTML = []

    def buffer_append(self, html):
        self.HTML.append(html)

    def buffer_htmlize(self, text, omit_first_p=False):
        if not text:
            return
        text = text.strip()
        if not text or text[0]=="<":
            return self.buffer_append(text)
        text = re.sub(r"(?:(?:^|\n)\s*){2,}", r"\n\n", text)
        first = True
        for item in text.split(r"\n\n"):
            if first and omit_first_p:
                self.buffer_append(item)
            else:
                self.buffer_append("<p>%s</p>" % item)
            first = False

    def buffer_inform(self, dotpath, **kargs):
        text = self.get_template(dotpath, **kargs)
        if text:
            html = self.format(text, **kargs)
            self.buffer_htmlize(html)

    def buffer_get(self):
        try:
            return "\n".join(self.HTML)
        finally:
            self.buffer_clear()

    def buffer_peek(self, what, **kargs):
        text = what.get_template("info.actor", peeked=what)
        if text:
            html = self.format(text, peeked=what, **kargs)
            self.buffer_append("<li>")
            self.buffer_htmlize(html, omit_first_p=True)
            self.buffer_append("</li>")


class Event1(Event):

    def __init__(self, actor):
        Event.__init__(self)
        self.actor = actor

    def context(self):
        context = super().context()
        context["actor"] = self.actor
        actor = self.actor
        if isinstance(actor, Containing):
            loc = actor
        elif hasattr(actor, "container"):
            loc = actor.container()
        else:
            loc = None
        context["location"] = loc
        return context

    def observers(self):
        cont = self.actor.container()
        if cont:
            for x in cont.contents():
                if x is not self.actor and x.is_player() and x.can_see():
                    yield x

    def inform(self, dotpath, **kargs):
        self.buffer_clear()
        self.buffer_inform(dotpath+".actor")
        html = self.buffer_get()
        if html:
            getattr(self.actor, self.SEND_ACTOR)(html)
        for observer in self.observers():
            self.buffer_clear()
            self.buffer_inform(dotpath+".observer", observer=observer)
            html = self.buffer_get()
            if html:
                getattr(observer, self.SEND_OBSERVER)(html)
                      

class Event2(Event1):

    def __init__(self, actor, object):
        Event1.__init__(self, actor)
        self.object = object

    def context(self):
        context = super().context()
        context["object"] = self.object
        if hasattr(self.object, "is_exit") and self.object.is_exit():
            context["exit"] = self.object
            context["portal"] = self.object.portal
        return context

    def get_event_templates(self):
        return self.object.get_event_templates()


class Event3(Event2):

    def __init__(self, actor, object, object2):
        Event2.__init__(self, actor, object)
        self.object2 = object2

    def context(self):
        context = super().context()
        context["object2"] = self.object2
        return context
