from enum import Enum
from typing import Optional


class ZoneType(Enum):
    "Diferent types of zones available"

    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


class Zone:
    def __init__(self, type: str):
        self.type: str = type
        
