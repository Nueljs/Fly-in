import sys
from parser import MapParser
from models import Network
from simulation import Simulation


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <filepath>")
        sys.exit(1)

    filepath: str = sys.argv[1]

    try:
        parser: MapParser = MapParser(filepath)
        network: Network = parser.parse()
        nb_drones: int = parser.nb_drones

        sim: Simulation = Simulation(network, nb_drones)
        sim.run()
    except Exception as e:
        print(f"{e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
