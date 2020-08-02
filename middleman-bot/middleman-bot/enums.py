from enum import Enum, IntEnum, Flag, auto

# ButtonCallbackData
class BCD(Flag):
    LIFT_STATE_NONE = auto()
    LIFT_STATE_WAREHOUSE = auto()
    LIFT_STATE_SHORE = auto()
    LIFT_STATE_OPENING = auto()
    LIFT_STATE_SITE = auto()
    LIFT_STATE_MISSING = auto()
    LIFT_STATE_READY = auto()

    REPLY_SEND_LIFT = auto()
    REPLY_CANCEL_LIFT = auto()

    REPLY_LIFT_UPDATE_STATE = auto()
    REPLY_LIFT_DELETE = auto()
    REPLT_LIFT_ADD_LINKS = auto()

    REPLY_USER_MORE = auto()
    REPLY_USER_END_LINK = auto()

# USER_DATA
class UD(Flag):
    NEW_LIFT = auto()
    SHIPMENT_ID = auto()

# BOT_DATA
class BD(Flag):
    LIFT_LIST = auto()
    LAST_ID = auto()

