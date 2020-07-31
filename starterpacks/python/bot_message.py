from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from enum import Enum


class Move(Enum):
    FORWARD = "FORWARD"
    TURN_LEFT = "TURN_LEFT"
    TURN_RIGHT = "TURN_RIGHT"


class MessageType(Enum):
    MOVE = "move"
    REGISTER = "register"


@dataclass_json
@dataclass
class BotMessage:
    type: MessageType
    action: Move = None
    tick: int = None
    token: str = None
    name: str = None
