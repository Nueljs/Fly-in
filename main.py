import sys
from parser import MapParser
from models import Network
from simulation import Simulation


def main() -> None:
    """
    Main entry of the program. Parses command-line arguments,
    loads the network map, and stats the simulation.
    """
    use_visual: bool = "--visual" in sys.argv
    clean_args: list[str] = [arg for arg in sys.argv[1:] if arg != "--visual"]

    if len(clean_args) != 1:
        print("Usage: python3 main.py <filepath> [--visual]")
        sys.exit(1)

    filepath: str = clean_args[0]

    try:
        parser: MapParser = MapParser(filepath)
        network: Network = parser.parse()
        nb_drones: int = parser.nb_drones

        sim: Simulation = Simulation(network, nb_drones, use_visual)
        sim.run()
    except Exception as e:
        print(f"{e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
