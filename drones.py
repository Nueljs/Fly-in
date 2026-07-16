from enum import Enum
from models import Zone


class DroneStatus(Enum):
    """Different status of the drones"""
    WAITING = "waiting"
    IN_TRANSIT = "in_transit"
    ARRIVED = "arrived"


class Drone:
    """Class that represents each drone in the network"""
    def __init__(self,
                 drone_id: str,
                 current_zone: Zone,
                 status: DroneStatus = DroneStatus.WAITING,
                 cooldown: int = 0) -> None:
        """
        Initializes a new drone with its starting zone, status, and cooldown.
        """
        self.drone_id: str = drone_id
        self.current_zone: Zone = current_zone
        self.status: DroneStatus = status
        self.cooldown: int = cooldown
        self.target_zone: Zone | None = None

    def __str__(self) -> str:
        """
        Define how the object is printed (ex: D1-waypoint1)
        """
        return f"{self.drone_id}-{self.current_zone.name}"
