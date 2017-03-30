# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from mud.events.failedaction import FailedActionEvent
from mud.models.mixins.propertied import Propertied

class Action(Propertied):

    def __init__(self):
        super().__init__()
        self.error = None
        self.add_prop(self.ACTION)

    def execute(self):
        if not self.subject.is_alive():
            return
        self.resolve()
        if self.error:
            self.add_prop(self.error)
            FailedActionEvent(self.subject, self).execute()
        else:
            self.perform()

    def perform(self):
        raise NotImplemented()

    def resolve(self):
        pass


class Action1(Action):

    def __init__(self, subject):
        super().__init__()
        self.subject = subject

    def resolve(self):
        super().resolve()
        if not self.subject.can_see():
            self.add_prop("cannot-see")

    def perform(self):
        self.EVENT(self.subject).execute()


class Action2(Action1):

    def __init__(self, subject, object):
        Action1.__init__(self, subject)
        self.object = object
        self.object_resolved = None

    def resolve(self):
        super().resolve()
        if not self.error:
            obj = self.resolve_object()
            if obj is not None:
                self.object_resolved = obj
            else:
                self.error = "cannot-find-object"

    def resolve_object(self):
        meth = getattr(self, "RESOLVE_OBJECT")
        return getattr(self.subject, meth)(name=self.object)

    def perform(self):
        self.EVENT(self.subject, self.object_resolved).execute()
        

class Action3(Action2):

    def __init__(self, subject, object, object2):
        Action2.__init__(self, subject, object)
        self.object2 = object2
        self.object2_resolved = None

    def resolve(self):
        super().resolve()
        if not self.error:
            obj = self.resolve_object2()
            if obj:
                self.object2_resolved = obj
            else:
                self.error = "cannot-find-object2"

    def resolve_object2(self):
        meth = getattr(self, "RESOLVE_OBJECT2")
        return getattr(self.subject, meth)(name=self.object2)

    def perform(self):
        self.EVENT(self.subject, self.object_resolved,
                   self.object2_resolved).execute()
