from models import Network


class MapParser:
    def __init__(self, filepath: str):
        self.filepath: str = filepath
        self.network: Network = Network()
        self.current_line: int = 0
        self.nb_drones: int = 0

    def parse(self) -> Network:
        with open(self.filepath, 'r') as f:
            for line in f:
                self.current_line = self.current_line + 1
                line = line.strip()
                if not line:
                    continue
                elif line.startswith("#"):
                    continue
                elif line.startswith("nb_drones"):
                    split_line = line.split(":")
                    if int(split_line[1]) > 0:
                        self.nb_drones = int(split_line[1])
                    else:
                        raise ValueError(f"Error at line {self.current_line}:"
                                          f"nb_drones must be greater than zero")
