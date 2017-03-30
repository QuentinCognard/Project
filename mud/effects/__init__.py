# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .changeprop import ChangePropEffect
from .go         import EnterPortalEffect, TraversePortalEffect, LeavePortalEffect, MoveEffect
from .death      import DeathEffect
from .close      import CloseEffect, CloseWithEffect
from .drop       import DropEffect, DropInEffect
from .info       import InfoEffect
from .inspect    import InspectEffect
from .inventory  import InventoryEffect
from .light      import LightOnEffect, LightOffEffect
from .look       import LookEffect
from .open       import OpenEffect, OpenWithEffect
from .push       import PushEffect
from .take       import TakeEffect
from .type       import TypeEffect
from .narrative  import NarrativeEffect
