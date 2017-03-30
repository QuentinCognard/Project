# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

import re
from .basic import Basic
import mud.game

RE_CALL = re.compile(r"^(?P<prop>(?:\w|[-_.])+)(?:\((?P<arg>[^)]*)\)|)$")

class Propertied(Basic):

    """mixin class that provides a way for a model to have properties that can
    be tested and modified."""

    #--------------------------------------------------------------------------
    # initialization
    #--------------------------------------------------------------------------
    
    def __init__(self, **kargs):
        super().__init__(**kargs)
        self._props = set()

    #--------------------------------------------------------------------------
    # initialization from YAML data
    #--------------------------------------------------------------------------

    def init_from_yaml(self, data, world):
        super().init_from_yaml(data, world)
        if "props" in data:
            self._props = set(data["props"])

    def update_from_yaml(self, data, world):
        super().update_from_yaml(data, world)
        if "props" in data:
            self._props = set(data["props"])

    #--------------------------------------------------------------------------
    # API for saving the dynamic part of objects to YAML (via JSON)
    #--------------------------------------------------------------------------

    def archive_into(self, obj):
        super().archive_into(obj)
        obj["props"] = list(self._props)

    #--------------------------------------------------------------------------
    # properties API
    #--------------------------------------------------------------------------

    def props_proxy(self):
        """returns the proxy object that actually holds the properties."""
        return self

    def has_props(self, props, context=None):
        """checks whether the model has all the given properties."""
        return all(self.has_prop(prop, context) for prop in props)

    def has_prop(self, prop, context=None):
        """checks whether the model has the given property.

        m.has_prop("+foo")
        m.has_prop("foo")
           checks that m has property "foo".
        m.has_prop("-foo")
           checks that m doesn't have property "foo"."""
        prefix = prop[0]
        if prefix == "+":
            return self._has_prop(prop[1:], context)
        if prefix == "-":
            return not self._has_prop(prop[1:], context)
        return self._has_prop(prop, context)

    def _has_prop(self, prop, context=None):
        """m._has_prop("actor:foo", context) looks up actor in context and
        delegates to it _has_prop("foo").  m._has_prop("=toto:foo") looks up
        toto (by id) in the world and delegates _has_prop("foo") to it.
        m._has_prop("foo") either tries m.has_prop_foo() if it exists, or
        m._has_prop_foo() if it exists, or checks if m has a property "foo"."""
        obj, prop = self._analyze_prop(prop, context)
        if obj is not self:
            return obj._has_prop(prop)
        obj = self.prop_proxy(prop)
        if obj is not self:
            return obj._has_prop(prop)
        m = RE_CALL.match(prop)
        p = m.group("prop")
        a = m.group("arg")
        args = () if a is None else (a,)
        mprop = self._sanitize_prop(p)
        meth = (getattr(self,  "has_prop_"+mprop, None) or
                getattr(self, "_has_prop_"+mprop, None))
        if meth:
            return meth(*args)
        elif args:
            raise Exception("_has_prop: %s" % prop)
        else:
            return prop in self._get_props()

    def _analyze_prop(self, prop, context):
        if ":" in prop:
            key, prop = prop.split(":", 1)
            if key[0] == "=":
                obj = mud.game.GAME.world[key[1:]]
            else:
                obj = context[key]
        else:
            obj = self
        return obj, prop

    def _sanitize_prop(self, prop):
        return re.sub(r"[^\w]+", "_", prop)

    def _get_props(self):
        return self.props_proxy()._props

    def prop_proxy(self, prop):
        """allow for fine-grained delegation of properties."""
        return self

    def add_prop(self, prop, context=None):
        obj, prop = self._analyze_prop(prop, context)
        if obj is not self:
            return obj.add_prop(prop, context)
        obj = self.prop_proxy(prop)
        if obj is not self:
            return obj.add_prop(prop, context)
        mprop = self._sanitize_prop(prop)
        meth = (getattr(self,  "add_prop_"+mprop, None) or
                getattr(self, "_add_prop_"+mprop, None))
        if meth:
            meth()
        else:
            self._get_props().add(prop)

    def remove_prop(self, prop, context=None):
        obj, prop = self._analyze_prop(prop, context)
        if obj is not self:
            return obj.remove_prop(prop, context)
        obj = self.prop_proxy(prop)
        if obj is not self:
            return obj.remove_prop(prop, context)
        mprop = self._sanitize_prop(prop)
        meth = (getattr(self,  "remove_prop_"+mprop, None) or
                getattr(self, "_remove_prop_"+mprop, None))
        if meth:
            meth()
        else:
            try:
                self._get_props().remove(prop)
            except KeyError:
                pass

    def change_prop(self, prop, context=None):
        prefix = prop[0]
        if prefix == "+":
            self.add_prop(prop[1:], context)
        elif prefix == "-":
            self.remove_prop(prop[1:], context)
        else:
            self.add_prop(prop, context)

    def set_props(self, props):
        for prop in props:
            # this way computed properties work too
            self.set_prop(prop)

    def get_props(self):
        return list(self._get_props())

    def change_props(self, props, context=None):
        for prop in props:
            self.change_prop(prop, context)

    #--------------------------------------------------------------------------
    # computed properties:
    # - empty		(purely observational)
    # - has-class(ClassName)
    #--------------------------------------------------------------------------

    def _has_prop_empty(self):
        return not self._contents

    def _add_prop_empty(self):
        raise NotImplemented()

    def _remove_prop_empty(self):
        raise NotImplemented()

    def _has_prop_has_class(self, cname):
        for x in self.__class__.__mro__:
            if cname == x.__name__:
                return True
        return False

    #--------------------------------------------------------------------------
    # check for certain capabilities
    #--------------------------------------------------------------------------

    def is_key_for(self, obj):
        """return True iff this is a key for obj."""
        self.has_prop("key-for-%s" % obj.id)
