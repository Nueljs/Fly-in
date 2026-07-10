from enum import Enum
from collections import deque


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

    @property
    def has_capacity(self) -> bool:
        if self.is_end:
            return True
        return len(self.curr_drones) < self.max_drones

    def enter_drone(self, drone_id: str) -> None:
        """Add a dron to the zone if there is capacity"""
        if self.has_capacity:
            self.curr_drones.append(drone_id)

    def exit_drone(self, drone_id: str) -> None:
        """Remove a drone from the zone if it's exists"""
        if drone_id in self.curr_drones:
            self.curr_drones.remove(drone_id)


class Connection:
    def __init__(self, zone1: Zone, zone2: Zone,
                 max_link_capacity: int = 1) -> None:
        self.zone1: Zone = zone1
        self.zone2: Zone = zone2
        self.max_link_capacity: int = max_link_capacity
        self.curr_drones: list[str] = []

    @property
    def has_capacity(self) -> bool:
        return len(self.curr_drones) < self.max_link_capacity

    def enter_drone(self, drone_id: str) -> None:
        """Add a dron to the connection if there is capacity"""
        if self.has_capacity:
            self.curr_drones.append(drone_id)

    def exit_drone(self, drone_id: str) -> None:
        """Remove a drone from the connection if it's exists"""
        if drone_id in self.curr_drones:
            self.curr_drones.remove(drone_id)


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

    def get_neighbors(self, current_zone: Zone,
                      check_capacity: bool = False) -> list[Zone]:
        """
        Finds all adjacent zones connected to the given zone
        """
        neighbors: list[Zone] = []
        for connection in self.connections:
            if current_zone == connection.zone1:
                if connection.zone2.zone_type != ZoneType.BLOCKED:
                    if not check_capacity or (connection.zone2.has_capacity
                                              and connection.has_capacity):
                        neighbors.append(connection.zone2)
            elif current_zone == connection.zone2:
                if connection.zone1.zone_type != ZoneType.BLOCKED:
                    if not check_capacity or (connection.zone1.has_capacity
                                              and connection.has_capacity):
                        neighbors.append(connection.zone1)
        return neighbors

    def building_path(self, end_zone: Zone,
                      came_from: dict[Zone, Zone | None]) -> list[Zone]:
        """
        Calculates the path using the dict who
        has the zones where the drones came
        """
        path: list[Zone] = []
        current: Zone | None = end_zone

        while current is not None:
            path.append(current)
            current = came_from[current]

        return path[::-1]

    def get_shortest_path(self, start: Zone, end: Zone) -> list[Zone]:
        """Find the shortest path between two zones using BFS"""
        queue: deque[Zone] = deque()
        queue.append(start)

        visited: set[Zone] = set()
        visited.add(start)

        came_from: dict[Zone, Zone | None] = {}
        came_from[start] = None

        while queue:
            curr_zone: Zone = queue.popleft()

            if curr_zone == end:
                return self.building_path(curr_zone, came_from)

            check_cap: bool = (curr_zone == start)
            neighbors: list[Zone] = self.get_neighbors(curr_zone, check_cap)
            for neighbor in neighbors:
                if neighbor not in visited:
                    came_from[neighbor] = curr_zone
                    visited.add(neighbor)
                    queue.append(neighbor)
        return []

    def get_connection(self, zone1: Zone, zone2: Zone) -> Connection:
        for conn in self.connections:
            if ((zone1 == conn.zone1 and zone2 == conn.zone2) or
                    (zone2 == conn.zone1 and zone1 == conn.zone2)):
                return conn
        raise ValueError("Error: Connection between zones not found")
