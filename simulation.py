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

        if self.network.start_zone:
            initial_path = self.network.get_shortest_path(
                self.network.start_zone, target_zone)
            if not initial_path:
                raise ValueError("Error: The graph is disconnected. No valid"
                                 " path to end_zone")

        while self._get_arrived_count() < len(self.drones):
            turn_moves: list[str] = []
            any_moved: bool = False

            for c in self.network.connections:
                c.used_this_turn = 0

            processed_this_turn: set[str] = set()
            progress_in_pass: bool = True

            while progress_in_pass:
                progress_in_pass = False

                for drone in self.drones:
                    if drone.drone_id in processed_this_turn:
                        continue

                    if drone.status == DroneStatus.ARRIVED:
                        processed_this_turn.add(drone.drone_id)
                        continue

                    if drone.cooldown > 0:
                        drone.cooldown = drone.cooldown - 1

                        if drone.cooldown == 0 and drone.target_zone:
                            curr_conn: Connection = (
                                self.network.get_connection(
                                        drone.current_zone, drone.target_zone))
                            curr_conn.exit_drone(drone.drone_id)
                            drone.target_zone.enter_drone(drone.drone_id)
                            drone.current_zone = drone.target_zone

                            if drone.current_zone.is_end:
                                drone.status = DroneStatus.ARRIVED
                            else:
                                drone.status = DroneStatus.WAITING

                            turn_moves.append(str(drone))
                            drone.target_zone = None

                        processed_this_turn.add(drone.drone_id)
                        any_moved = True
                        progress_in_pass = True
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
                        else:
                            conn.exit_drone(drone.drone_id)
                            conn.used_this_turn += 1
                            next_zone.enter_drone(drone.drone_id)
                            drone.current_zone = next_zone
                            if drone.current_zone.is_end:
                                drone.status = DroneStatus.ARRIVED
                            else:
                                drone.status = DroneStatus.WAITING
                            turn_moves.append(str(drone))

                        processed_this_turn.add(drone.drone_id)
                        any_moved = True
                        progress_in_pass = True
                    else:
                        drone.status = DroneStatus.WAITING

            if not any_moved and self._get_arrived_count() < len(self.drones):
                raise RuntimeError(
                    f"Simulation aborted at turn {self.turn}: "
                    "Irrecoverable deadlock detected."
                )

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
