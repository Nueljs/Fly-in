from enum import Enum


class ZoneType(Enum):
    "Diferent types of zones available"

    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


class Zone:
    def __init__(self, name: str, x: int, y: int,
                 zone_type: ZoneType = ZoneType.NORMAL,
                 color: str | None = None,
                 max_drones: int = 1) -> None:
        self.name: str = name
        self.x: int = x
        self.y: int = y
        self.zone_type: ZoneType = zone_type
        self.color: str | None = color
        self.max_drones: int = max_drones
        self.is_start: bool = False
        self.is_end: bool = False
        self.curr_drones: list[str] = []

    def hub_cost(self) -> int:
        """Returns the turn cost to move into this zone"""
        if self.zone_type is ZoneType.RESTRICTED:
            return (2)
        return (1)


class Connection:
    def __init__(self, zone1: Zone, zone2: Zone,
                 max_link_capacity: int = 1) -> None:
        self.zone1: Zone = zone1
        self.zone2: Zone = zone2
        self.max_link_capacity: int = max_link_capacity
        self.curr_drones: list[str] = []


class Network:
    def __init__(self) -> None:
        self.zones: dict[str, Zone] = {}
        self.connections: list[Connection] = []
        self.start_zone: Zone | None = None
        self.end_zone: Zone | None = None

    def add_zone(self, zone: Zone) -> None:
        self.zones[zone.name] = zone
        if zone.is_start:
            self.start_zone = zone
        elif zone.is_end:
            self.end_zone = zone

    def add_connection(self, connection: Connection) -> None:
        self.connections.append(connection)
