import unittest
from unittest.mock import patch, mock_open

# Importamos tu clase (asumiendo que tu archivo se llama parser.py)
from parser import MapParser


class TestMapParser(unittest.TestCase):

    def test_01_valid_map_parsing(self) -> None:
        """Prueba que un mapa perfecto se lee e instancia sin errores."""
        valid_map: str = (
            "# Mapa de prueba perfecto\n"
            "nb_drones: 5\n"
            "start_hub: salida 0 0 [zone=normal color=green]\n"
            "hub: pasillo 5 5 [zone=restricted max_drones=2]\n"
            "end_hub: meta 10 10 [zone=priority]\n"
            "connection: salida-pasillo [max_link_capacity=3]\n"
            "connection: pasillo-meta\n"
        )
        # Interceptamos la llamada a open() y le pasamos nuestro string
        with patch("builtins.open", mock_open(read_data=valid_map)):
            parser = MapParser("dummy.txt")
            network = parser.parse()

            # Comprobaciones de que todo se guardó donde debía
            self.assertEqual(parser.nb_drones, 5)
            self.assertIn("salida", network.zones)
            self.assertTrue(network.zones["salida"].is_start)
            
            # Comprueba la lógica de tu clase Zone
            self.assertEqual(network.zones["pasillo"].hub_cost(), 2)
            self.assertEqual(network.zones["pasillo"].max_drones, 2)
            
            # Comprueba las conexiones
            self.assertEqual(len(network.connections), 2)
            self.assertEqual(network.connections[0].max_link_capacity, 3)
            self.assertEqual(network.connections[1].max_link_capacity, 1)

    def test_02_missing_start_or_end(self) -> None:
        """Prueba que salte error si el mapa no tiene salida o meta."""
        bad_map: str = (
            "nb_drones: 2\n"
            "start_hub: salida 0 0\n"
            "hub: pasillo 5 5\n"
            "connection: salida-pasillo\n"
        )
        with patch("builtins.open", mock_open(read_data=bad_map)):
            parser = MapParser("dummy.txt")
            # Verifica que el código levante un ValueError
            with self.assertRaises(ValueError):
                parser.parse()

    def test_03_invalid_connection_zones(self) -> None:
        """Prueba que falle si intentas conectar una zona que no existe."""
        bad_map: str = (
            "nb_drones: 2\n"
            "start_hub: salida 0 0\n"
            "end_hub: meta 10 10\n"
            "connection: salida-fantasma\n"
        )
        with patch("builtins.open", mock_open(read_data=bad_map)):
            parser = MapParser("dummy.txt")
            with self.assertRaises(ValueError):
                parser.parse()

    def test_04_invalid_coordinates(self) -> None:
        """Prueba que falle si las coordenadas de una zona no son números."""
        bad_map: str = (
            "nb_drones: 2\n"
            "start_hub: salida cero cero\n"
            "end_hub: meta 10 10\n"
        )
        with patch("builtins.open", mock_open(read_data=bad_map)):
            parser = MapParser("dummy.txt")
            with self.assertRaises(ValueError):
                parser.parse()

    def test_05_invalid_nb_drones(self) -> None:
        """Prueba que falle si el número de drones es texto o negativo."""
        bad_map: str = (
            "nb_drones: cinco\n"
            "start_hub: salida 0 0\n"
            "end_hub: meta 10 10\n"
        )
        with patch("builtins.open", mock_open(read_data=bad_map)):
            parser = MapParser("dummy.txt")
            with self.assertRaises(ValueError):
                parser.parse()


if __name__ == "__main__":
    # Esta línea ejecuta todos los tests automáticamente al llamar al script
    unittest.main(verbosity=2)