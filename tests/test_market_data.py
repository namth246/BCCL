import unittest

from market_data import build_market_week


class MarketWeekTests(unittest.TestCase):
    def test_build_market_week_normalizes_indices_and_foreign_flow(self):
        index_rows = {
            "VNINDEX": [("2026-08-24", 1788.78), ("2026-08-28", 1832.12)],
            "VN30": [("2026-08-24", 1900.0), ("2026-08-28", 1920.0)],
            "HNXINDEX": [("2026-08-24", 300.0), ("2026-08-28", 303.0)],
            "UPCOMINDEX": [("2026-08-24", 100.0), ("2026-08-28", 102.0)],
        }
        foreign_rows = [("2026-08-25", 276677170000), ("2026-08-26", -36997410000)]

        result = build_market_week(index_rows, [1000000000000, 2000000000000], foreign_rows)

        self.assertEqual(result["indices"][0], {"name": "VNINDEX", "close": "1,832.12", "change": "+43.34", "percent": "+2.42%"})
        self.assertEqual(result["trading_value"], "1,500")
        self.assertEqual(result["foreign_flow"], [{"date": "25/08", "value": 277}, {"date": "26/08", "value": -37}])


if __name__ == "__main__":
    unittest.main()
