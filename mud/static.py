# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

import yaml, os.path

STATIC = yaml.load(open(os.path.join(os.path.dirname(__file__), "static.yml")))
