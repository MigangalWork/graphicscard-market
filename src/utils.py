
from enum import Enum


class Action(Enum):
    BUY = 0
    SELL = 1
    HOLD = 2

operation_sign: dict = {
    Action.BUY: -1,
    Action.SELL: 1
}