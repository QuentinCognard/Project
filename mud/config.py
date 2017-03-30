# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

import os, os.path

ROOTDIR = os.path.dirname(os.path.dirname(__file__))
DATADIR = os.path.join(ROOTDIR,".datadir")
try:
    os.mkdir(DATADIR)
except:
    pass
