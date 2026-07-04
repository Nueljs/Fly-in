from models import Network, Zone, ZoneType, Connection


class MapParser:
    def __init__(self, filepath: str):
        """Class used to parser maps"""
        self.filepath: str = filepath
        self.network: Network = Network()
        self.current_line: int = 0
        self.nb_drones: int = 0

    def _parse_zone(self, line: str) -> Zone:
        """Method used to parser zones"""
        splited_data: list = line.split("[")
        color: str | None = None
        max_drones: int = 1
        zone_enum: ZoneType = ZoneType.NORMAL
        if len(splited_data) > 1:
            metadata: str = splited_data[1]
            metadata = metadata.replace("]", "")
            split_metadata = metadata.split()
            dict_metadata: dict = {}
            for item in split_metadata:
                meta_list = item.split("=")
                if len(meta_list) == 2:
                    dict_metadata[meta_list[0]] = meta_list[1]
                else:
                    raise ValueError(f"Error on line {self.current_line}:"
                                     " invalid format in metadata use"
                                     " [key=value]")
            if "zone" in dict_metadata:
                try:
                    zone_enum = ZoneType(dict_metadata["zone"])
                except ValueError:
                    raise ValueError(f"Error on line {self.current_line}: "
                                     "invalid zone type")
            if "color" in dict_metadata:
                color = dict_metadata["color"]
            if "max_drones" in dict_metadata:
                try:
                    max_drones = int(dict_metadata["max_drones"])
                except ValueError:
                    raise ValueError(f"Error on line {self.current_line}: "
                                     "max_drones must be an int")
        data_list: list = [data.strip() for data in splited_data[0].split()]
        if len(data_list) != 4:
            raise ValueError(f"Error on line {self.current_line}"
                             " invalid zone format")
        zone_type, name, str_x, str_y = data_list
        try:
            x = int(str_x)
            y = int(str_y)
        except ValueError:
            raise ValueError(f"Error on line {self.current_line},"
                             " the coordenates must be a int")
        new_zone = Zone(name, x, y, zone_enum, color, max_drones)

        if zone_type == "start_hub:":
            new_zone.is_start = True
        elif zone_type == "end_hub:":
            new_zone.is_end = True
        elif zone_type != "hub:":
            raise ValueError(f"Error on line {self.current_line}"
                             f"invalid hub type '{zone_type}'")

        return new_zone

    def _parse_connection(self, line: str) -> Connection:
        """Method used to parser connections"""
        max_link_capacity: int = 1
        line_parts: list[str] = line.split("[")
        parsed_meta: dict[str, str] = {}

        if len(line_parts) > 1:
            raw_metadata: str = line_parts[1].replace("]", "")
            metadata_items: list[str] = raw_metadata.split()

            for item in metadata_items:
                key_value: list[str] = item.split("=")
                if len(key_value) == 2:
                    parsed_meta[key_value[0]] = key_value[1]
                else:
                    raise ValueError(f"Error on line {self.current_line}:"
                                     " invalid format in metadata use"
                                     " [key=value]")

            if "max_link_capacity" in parsed_meta:
                try:
                    max_link_capacity = int(
                        parsed_meta["max_link_capacity"])
                except ValueError:
                    raise ValueError(f"Error on line {self.current_line} "
                                     "max_link_capacity must be an int")
        data_list: list[str] = line_parts[0].replace("-", " ").split()
        if len(data_list) != 3:
            raise ValueError(f"Error on line {self.current_line} "
                             "invalid format on connection data")
        zone1_name: str = data_list[1]
        zone2_name: str = data_list[2]
        if (zone1_name not in self.network.zones
                or zone2_name not in self.network.zones):
            raise ValueError(f"Error on line {self.current_line}: Cannot"
                             " connect undefined zones")

        zone1_obj: Zone = self.network.zones[zone1_name]
        zone2_obj: Zone = self.network.zones[zone2_name]

        return Connection(zone1_obj, zone2_obj, max_link_capacity)

    def parse(self) -> Network:
        """Main method where the zones and connections are parser"""
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
                        raise ValueError(f"Error at line {self.current_line}:"
                                         " nb_drones must be an int")
                    if value_drone > 0:
                        self.nb_drones = value_drone
                    else:
                        raise ValueError(f"Error at line {self.current_line}:"
                                         f"nb_drones must be greater than "
                                         "zero")
                elif line.startswith(("hub:", "start_hub:", "end_hub:")):
                    created_zone = self._parse_zone(line)
                    self.network.add_zone(created_zone)
                elif line.startswith("connection:"):
                    created_connection = self._parse_connection(line)
                    self.network.add_connection(created_connection)
        if not self.network.start_zone or not self.network.end_zone:
            raise ValueError(f"Error on line {self.current_line}: must"
                             " be exits a start point and an end point")
        return self.network
