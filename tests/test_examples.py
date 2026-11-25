import unittest
from datetime import date

from examples.scd2_reference import apply_snapshot
from tools.check_names import invalid_names
from tools.impact import impact


class Scd2Tests(unittest.TestCase):
    def test_change_null_and_idempotent_replay(self):
        d1, d2 = date(2026, 1, 1), date(2026, 2, 1)
        first = apply_snapshot([], [{"customer_id": 1, "region": None}], d1)
        second = apply_snapshot(first, [{"customer_id": 1, "region": "norte"}], d2)
        self.assertEqual(second[0]["valid_to"], d2)
        self.assertIsNone(first[0]["valid_to"])
        self.assertEqual(second, apply_snapshot(second, [{"customer_id": 1, "region": "norte"}], d2))

    def test_invalid_snapshots_do_not_change_input(self):
        first = apply_snapshot([], [{"customer_id": 1, "region": "norte"}], date(2026, 2, 1))
        for snapshot, day in [
            ([{"customer_id": 1, "region": "sur"}], date(2026, 2, 1)),
            ([{"customer_id": 1, "region": "sur"}], date(2026, 1, 1)),
            ([{"customer_id": 1, "region": "x"}, {"customer_id": 1, "region": "y"}], date(2026, 3, 1)),
        ]:
            with self.assertRaises(ValueError):
                apply_snapshot(first, snapshot, day)
            self.assertIsNone(first[0]["valid_to"])


class ToolsTests(unittest.TestCase):
    def test_names_and_non_list(self):
        self.assertEqual(invalid_names(["silver_ventas", "Ventas", "gold_"]), ["Ventas", "gold_"])
        with self.assertRaises(ValueError):
            invalid_names("silver_ventas")

    def test_impact_follows_downstream_and_stops_cycles(self):
        edges = [{"from": "a", "to": "b"}, {"from": "b", "to": "c"},
                 {"from": "c", "to": "a"}, {"from": "x", "to": "a"}]
        self.assertEqual([[e["to"] for e in p] for p in impact(edges, "a")],
                         [["b"], ["b", "c"]])


if __name__ == "__main__":
    unittest.main()
