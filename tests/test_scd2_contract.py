import unittest
from datetime import date, datetime

from corporate_scd2.delta import validate_config


class ConfigurationTests(unittest.TestCase):
    def test_valid_config(self):
        validate_config("catalogo.esquema.clientes", ["id"], ["region"], date(2026, 1, 1))

    def test_rejects_unsafe_or_ambiguous_names(self):
        for target, keys, attributes in [
            ("catalogo.tabla", ["id"], ["region"]),
            ("catalogo.esquema.tabla;DROP", ["id"], ["region"]),
            ("catalogo.esquema.tabla", ["id"], ["ID"]),
            ("catalogo.esquema.tabla", ["id"], ["valid_to"]),
            ("catalogo.esquema.tabla", ["id"], ["__scd2_insert"]),
            ("catalogo.esquema.tabla", [], ["region"]),
        ]:
            with self.subTest(target=target, keys=keys, attributes=attributes):
                with self.assertRaises(ValueError):
                    validate_config(target, keys, attributes, date(2026, 1, 1))

    def test_rejects_datetime_as_effective_date(self):
        with self.assertRaises(ValueError):
            validate_config("catalogo.esquema.tabla", ["id"], ["region"], datetime(2026, 1, 1))


if __name__ == "__main__":
    unittest.main()
