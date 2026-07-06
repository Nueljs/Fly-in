from models import Network, Zone
from drones import Drone, DroneStatus


class Simulation:
    def __init__(self,
                 network: Network,
                 nb_drones: int) -> None:
        self.network: Network = network
        self.turn: int = 1
        self.drones: list[Drone] = []

        self._spawn_drones(nb_drones)

    def _spawn_drones(self, nb_drones: int) -> None:
        """
        Instantiates the rquired number of drones and places them
        at the starting of the network
        """
        if self.network.start_zone is None:
            raise ValueError("Simulation requires a start_zone")
        for i in range(1, nb_drones + 1):
            id_drone: str = f"D{i}"
            drone: Drone = Drone(id_drone, self.network.start_zone)
            self.drones.append(drone)

    def run(self) -> None:
        while self._get_arrived_count() < len(self.drones):
            print(f"Turn {self.turn}")
            for drone in self.drones:
                print(drone)
                if drone.cooldown > 0:
                    drone.cooldown = drone.cooldown - 1
            self.turn = self.turn + 1

    def _get_arrived_count(self) -> int:
        return len(list(filter(lambda drone: drone.status ==
                               DroneStatus.ARRIVED, self.drones)))
