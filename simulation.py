from models import Network, Zone, Connection, ZoneType
from drones import Drone, DroneStatus
from visualizer import Visualizer


class Simulation:
    """
    Orchestrates the execution of drone movements across the network turn
    by turn.
    """
    def __init__(self,
                 network: Network,
                 nb_drones: int,
                 use_visual: bool = False) -> None:
        """
        Initializes the simulation state, spawns drones,
        and sets up the visualizer.
        """
        self.network: Network = network
        self.turn: int = 1
        self.drones: list[Drone] = []
        self.use_visual: bool = use_visual

        self._spawn_drones(nb_drones)

        self.visualizer: Visualizer | None = None
        if self.use_visual:
            self.visualizer = Visualizer(self.network, self.drones)

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
        """
        Executes the main simulation loop, calculating paths and moving drones
        until finished.
        """
        target_zone: Zone | None = self.network.end_zone
        if target_zone is None:
            raise ValueError("Simulation requires an end_zone to run")

        while self._get_arrived_count() < len(self.drones):
            turn_moves: list[str] = []

            for drone in self.drones:
                if drone.status == DroneStatus.ARRIVED:
                    continue

                if drone.cooldown > 0:
                    drone.cooldown = drone.cooldown - 1

                    if drone.cooldown == 0 and drone.target_zone is not None:
                        curr_conn: Connection = self.network.get_connection(
                                    drone.current_zone, drone.target_zone)
                        curr_conn.exit_drone(drone.drone_id)
                        drone.target_zone.enter_drone(drone.drone_id)
                        drone.current_zone = drone.target_zone
                        if drone.current_zone.is_end:
                            drone.status = DroneStatus.ARRIVED
                        else:
                            drone.status = DroneStatus.WAITING
                        turn_moves.append(str(drone))
                        drone.target_zone = None
                    continue

                path: list[Zone] = self.network.get_shortest_path(
                                drone.current_zone, target_zone)

                if len(path) > 1:
                    next_zone: Zone = path[1]
                    conn: Connection = self.network.get_connection(
                                        drone.current_zone, next_zone)
                    drone.current_zone.exit_drone(drone.drone_id)
                    conn.enter_drone(drone.drone_id)
                    if next_zone.zone_type == ZoneType.RESTRICTED:
                        drone.cooldown = 1
                        drone.status = DroneStatus.IN_TRANSIT
                        drone.target_zone = next_zone
                        conn_name: str = (f"{drone.current_zone.name}-"
                                          f"{next_zone.name}")
                        turn_moves.append(f"{drone.drone_id}-{conn_name}")
                        continue
                    conn.exit_drone(drone.drone_id)
                    next_zone.enter_drone(drone.drone_id)
                    drone.current_zone = next_zone
                    if drone.current_zone.is_end:
                        drone.status = DroneStatus.ARRIVED
                    turn_moves.append(str(drone))
                else:
                    drone.status = DroneStatus.WAITING
            if turn_moves:
                print(f"Turn {self.turn} " + " ".join(turn_moves))

            if self.use_visual and self.visualizer is not None:
                self.visualizer.render(self.turn)

            self.turn = self.turn + 1

    def _get_arrived_count(self) -> int:
        """
        Returns the total number of drones that have successfully reached
        the end zone.
        """
        return len(list(filter(lambda drone: drone.status ==
                               DroneStatus.ARRIVED, self.drones)))
