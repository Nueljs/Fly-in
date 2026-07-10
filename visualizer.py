from models import Network
from drones import Drone


class Visualizer:
    COLORS: dict[str, str] = {
        "red": "\033[91m",
        "green": "\033[92m",
        "blue": "\033[94m",
        "yellow": "\033[93m",
        "gray": "\033[90m",
        "reset": "\033[0m"
    }

    def __init__(self, network: Network, drones: list[Drone]) -> None:
        self.network: Network = network
        self.drones: list[Drone] = drones
        self.max_x, self.max_y = self._get_grid_limits()

    def _get_grid_limits(self) -> tuple[int, int]:
        max_x: int = 0
        max_y: int = 0

        for zone in self.network.zones.values():
            if zone.x > max_x:
                max_x = zone.x
            if zone.y > max_y:
                max_y = zone.y
        return (max_x + 1, max_y + 1)

    def render(self, turn: int) -> None:
        print(f"\n{self.COLORS['yellow']}=== TURN {turn} ==="
              f"{self.COLORS['reset']}")

        matrix: list[list[str]] = [
            ["    " for _ in range(self.max_x)] for _ in range(self.max_y)
            ]
        