from models import Network, Zone


class MapParser:
    def __init__(self, filepath: str):
        self.filepath: str = filepath
        self.network: Network = Network()
        self.current_line: int = 0
        self.nb_drones: int = 0

    def _parse_zone(self, line: str) -> Zone:
        splited_data: list = line.split("[")
        if len(splited_data) > 1:
            metadata: str = splited_data[1]
            metadata.replace("]", "")
            splited_metadata = metadata.split()
            dict_metadata: dict = {}
            for item in splited_metadata:
                meta_list = item.split("=")
                if len(meta_list) == 2:
                    dict_metadata[meta_list[0]] = meta_list[1]
                else:
                    raise ValueError(f"Error on line {self.current_line}:"
                                       " invalid format in metadata use [key=value]")
            if "zone" in dict_metadata:
                zone = dict_metadata["zone"]
            if "color" in dict_metadata:
                color = dict_metadata["color"]
            if "max_drones" in dict_metadata:
                try:
                    max_drones = int(dict_metadata["max_drones"])
                except ValueError:
                    raise ValueError(f"Error on line f{self.current_line}: "
                                     "max_drones must be an int")
        data_list: list = [data.strip() for data in splited_data[0].split()]
        zone_type, name, str_x, str_y = data_list
        try:
            x = int(str_x)
            y = int(str_y)
        except ValueError:
            raise ValueError(f"Error on line {self.current_line},"
                             " the coordenates must be a int")

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
                    try:
                        value_drone = int(split_line[1])
                    except ValueError:
                        raise ValueError(f"Error at line {self.current_line}: nb_drones must be an int")
                    if value_drone > 0:
                        self.nb_drones = value_drone
                    else:
                        raise ValueError(f"Error at line {self.current_line}:"
                                        f"nb_drones must be greater than zero")

