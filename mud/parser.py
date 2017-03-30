# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

class Parser:
    
    def __init__(self, rules):
        """A rule is pair (ACTIONCLASS, PATTERN). see e.g. mud.games.iut.
        """
        import re
        self.rules = [(a,re.compile(p+"$")) for (a,p) in rules]

    def parse(self, actor, text):
        """Returns a pair (ACTION,TEXT) where ACTION is the instance of the
        action class for a matching rule.  The instance is constructed by
        calling the action constructor with the actor as first argument, and
        the (text of the) capturing groups as further arguments.  TEXT is
        the normalized version of the input, obtained by lowercasing, turning
        apostrophes into spaces, and ensuring that words are separated by
        single spaces.

        If no rule matched, then None,TEXT is returned.  
        """
        text = " ".join(text.split("'"))
        text = " ".join(text.strip().lower().split())
        for action,pattern in self.rules:
            m = pattern.match(text)
            if m:
                return action(actor, *m.groups()),text
        return None,text
