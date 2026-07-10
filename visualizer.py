from models import Network
from drones import Drone, DroneStatus

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
        self.network = network
        self.drones = drones
        
        # Obtenemos los límites reales (incluyendo negativos)
        self.min_x, self.max_x, self.min_y, self.max_y = self._get_grid_limits()
        
        # Escalamos x2 el tamaño para crear "huecos" físicos para las carreteras
        self.grid_w = (self.max_x - self.min_x) * 2 + 1
        self.grid_h = (self.max_y - self.min_y) * 2 + 1

    def _get_grid_limits(self) -> tuple[int, int, int, int]:
        # Pythonic way de buscar mínimos y máximos
        zones = list(self.network.zones.values())
        min_x = min(z.x for z in zones)
        max_x = max(z.x for z in zones)
        min_y = min(z.y for z in zones)
        max_y = max(z.y for z in zones)
        return min_x, max_x, min_y, max_y

    def render(self, turn: int) -> None:
        print(f"\n{self.COLORS['yellow']}=== TURN {turn} ==={self.COLORS['reset']}")

        # 1. Crear matriz vacía. Usamos 6 espacios "      " para alinear bien
        grid: list[list[str]] = [
            ["      " for _ in range(self.grid_w)] for _ in range(self.grid_h)
        ]

        # 2. Dibujar Zonas y Drones aterrizados
        for zone in self.network.zones.values():
            # Aplicamos el Offset y multiplicamos x2 para espaciar el mapa
            px = (zone.x - self.min_x) * 2
            py = (zone.y - self.min_y) * 2

            # Recolectamos los drones que están AHORA MISMO en esta zona
            drones_here = [d for d in self.drones 
                           if d.current_zone == zone and d.status != DroneStatus.IN_TRANSIT]

            # Formateamos el interior para que siempre ocupe 4 caracteres
            if len(drones_here) == 0:
                inner_txt = "    "
            elif len(drones_here) == 1:
                inner_txt = f"{drones_here[0].drone_id}".center(4)
            else:
                inner_txt = f"{len(drones_here)}D".center(4) # Ej: " 2D "

            cell_text = f"[{inner_txt}]"

            # Coloreamos
            if zone.color and zone.color in self.COLORS:
                c_code = self.COLORS[zone.color]
                r_code = self.COLORS["reset"]
                cell_text = f"{c_code}{cell_text}{r_code}"

            grid[py][px] = cell_text

        # 3. Dibujar Drones en Tránsito (en los huecos de las carreteras)
        for drone in self.drones:
            if drone.status == DroneStatus.IN_TRANSIT and drone.target_zone:
                px1 = (drone.current_zone.x - self.min_x) * 2
                py1 = (drone.current_zone.y - self.min_y) * 2
                px2 = (drone.target_zone.x - self.min_x) * 2
                py2 = (drone.target_zone.y - self.min_y) * 2

                # Ahora el punto medio caerá exactamente en una celda vacía real
                mid_x = (px1 + px2) // 2
                mid_y = (py1 + py2) // 2

                # Lo pintamos centrado a 6 caracteres para no desalinear
                grid[mid_y][mid_x] = f"{drone.drone_id}".center(6)

        # 4. Imprimir la matriz
        for row in grid:
            print("".join(row))
        print("\n")