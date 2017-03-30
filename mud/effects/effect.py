# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from mud.models.mixins.propertied import Propertied
import mud.game

class Effect(Propertied):

    def __init__(self, yaml, context):
        super().__init__()
        self.yaml = yaml
        self.context = context

    def context(self):
        return self.context

    def resolve(self, key):
        val = self.yaml.get(key)
        if val is None:
            return self.context[key]
        # anything but a string needs no further interpretation
        if not isinstance(val, str):
            return val
        # ref to a world object
        if val[0] == "=":
            return mud.game.GAME.world[val[1:]]
        # literal string
        if val[0] == "/":
            assert val[-1] == "/"
            return val[1:-1]
        # ref to a context object
        return self.context[val]

    @staticmethod
    def make_effect(yaml, context):
        cls = yaml["type"]
        import mud.effects
        cls = mud.effects.__dict__[cls]
        eff = cls(yaml, context)
        eff.init_from_yaml(yaml, mud.game.GAME.world)
        return eff

    @staticmethod
    def make_effects(yamls, context):
        if not yamls:
            return
        if not isinstance(yamls, list):
            yamls = [yamls]
        for yaml in yamls:
            effect = Effect.make_effect(yaml, context)
            props = yaml.get("props")
            if props is None or effect.has_props(props, context):
                yield effect

    def execute(self):
        self.to_event().execute()

    def to_event(self):
        event = self.make_event()
        self.init_event(event)
        return event

    def init_event(self, event):
        props = self.yaml.get("event-props")
        if props:
            if isinstance(props, str):
                props = [props]
            event.add_props(props)


class Effect1(Effect):

    def __init__(self, yaml, context):
        super().__init__(yaml, context)
        self.actor = self.resolve_actor()

    def resolve_actor(self):
        return self.resolve("actor")

    def make_event(self):
        return self.EVENT(self.actor)



class Effect2(Effect1):

    def __init__(self, yaml, context):
        super().__init__(yaml, context)
        self.object = self.resolve_object()

    def resolve_object(self):
        return self.resolve("object")

    def make_event(self):
        return self.EVENT(self.actor, self.object)



class Effect3(Effect2):

    def __init__(self, yaml, context):
        super().__init__(yaml, context)
        self.object2 = self.resolve_object2()

    def resolve_object2(self):
        return self.resolve("object2")

    def make_event(self):
        return self.EVENT(self.actor, self.object, self.object2)
