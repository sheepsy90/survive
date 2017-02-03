from server.scripting.intern.AlternateBetweenTwoLasers import AlternateBetweenTwoLasers
from server.scripting.intern.DisableLasersForever import DisableLasersForever
from server.scripting.intern.DisableLasersShortly import DisableLasersShortly
from server.scripting.intern.DoorHandlerAND import DoorHandlerAND
from server.scripting.usable.DigitalLockWithState import DigitalLockWithState
from server.scripting.usable.DigitalLockWithStateResetsAutomatically import DigitalLockWithStateResetsAutomatically
from server.scripting.usable.DigitalLockWithoutState import DigitalLockWithoutState

NO_AREA_CHANGE = 1
AREA_CHANGE = 2
FREE = 3
BLOCKED = 4
NOT_LOGGED_IN = 5
SRV_NO_MOVED = 6
SRV_MOVED = 7
CRAFTING_NOT_POSSIBLE = 8
CRAFTING_SUCCESS_DUMMY = 9
CRAFTING_SUCCESS_NORMAL = 10
GUARD_DENYS = 11
GUARD_ALLOWS = 12
SRV_NO_MOVED_OPEN_CONTAINER = 13
SRV_NO_MOVED_ALREADY_MOVING = 14

USABLE_SCRIPT_MAPPING = {
    DigitalLockWithoutState.LABEL_KEY: DigitalLockWithoutState,
    DigitalLockWithState.LABEL_KEY: DigitalLockWithState,
    DigitalLockWithStateResetsAutomatically.LABEL_KEY: DigitalLockWithStateResetsAutomatically
}

INTERNAL_SCRIPT_MAPPING = {
    DisableLasersForever.LABEL_KEY: DisableLasersForever,
    DisableLasersShortly.LABEL_KEY: DisableLasersShortly,
    DoorHandlerAND.LABEL_KEY: DoorHandlerAND,
    AlternateBetweenTwoLasers.LABEL_KEY: AlternateBetweenTwoLasers
}


class EnemySystemQueueConstants():

    CHANGED_ENEMIES = "CHANGED_ENEMIES"
    MOVING_ENEMIES = "MOVING_ENEMIES"
    ATTACKING_ENEMIES = "ATTACKING_ENEMIES"

