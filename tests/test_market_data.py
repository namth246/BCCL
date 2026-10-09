import unittest

from market_data import build_foreign_rankings, build_market_week, fetch_foreign_rankings, foreign_trade_query_start, select_latest_five_sessions


class MarketWeekTests(unittest.TestCase):
    def test_foreign_trade_query_start_includes_report_week_first_session(self):
        self.assertEqual(foreign_trade_query_start("2026-08-24"), "2026-08-23")

    def test_fetch_foreign_rankings_returns_available_data_when_five_sessions_are_missing(self):
        class Frame:
            def __init__(self, rows): self.rows = rows
            @property
            def empty(self): return not self.rows
            def __getitem__(self, _): return self
            def to_dict(self, _): return self.rows

        class Ranking:
            def foreign_buy(self, date, limit): return Frame([{"symbol": date[-2:], "net_value": 1_000_000_000}])
            def foreign_sell(self, date, limit): return Frame([{"symbol": f"S{date[-2:]}", "net_value": -1_000_000_000}])

        result = fetch_foreign_rankings(["2026-09-01", "2026-09-02"], ranking=Ranking())

        self.assertEqual(result["top_buy"], [{"ticker": "02", "value": 1}, {"ticker": "01", "value": 1}])

    def test_fetch_foreign_rankings_skips_missing_session_and_uses_older_session(self):
        class Frame:
            def __init__(self, rows): self.rows = rows
            @property
            def empty(self): return not self.rows
            def __getitem__(self, _): return self
            def to_dict(self, _): return self.rows

        class Ranking:
            def foreign_buy(self, date, limit): return Frame([] if date == "2026-08-28" else [{"symbol": date[-2:], "net_value": 1_000_000_000}])
            def foreign_sell(self, date, limit): return Frame([] if date == "2026-08-28" else [{"symbol": f"S{date[-2:]}", "net_value": -1_000_000_000}])

        result = fetch_foreign_rankings([
            "2026-08-27", "2026-08-28", "2026-08-31", "2026-09-01", "2026-09-02", "2026-09-03",
        ], ranking=Ranking())

        self.assertEqual([row["ticker"] for row in result["top_buy"]], ["03", "02", "01", "31", "27"])
        self.assertEqual([row["ticker"] for row in result["top_sell"]], ["S03", "S02", "S01", "S31", "S27"])

    def test_select_latest_five_sessions_uses_the_latest_trading_dates(self):
        sessions = [
            "2026-08-27", "2026-08-28", "2026-08-31", "2026-09-01",
            "2026-09-02", "2026-09-03", "2026-09-04",
        ]

        result = select_latest_five_sessions(sessions)

        self.assertEqual(result, ["2026-08-31", "2026-09-01", "2026-09-02", "2026-09-03", "2026-09-04"])

    def test_build_foreign_rankings_aggregates_five_sessions_and_keeps_top_five(self):
        ranking_rows = [
            {"symbol": "AAA", "net_value": 2_200_000_000},
            {"symbol": "AAA", "net_value": 1_100_000_000},
            {"symbol": "BBB", "net_value": 9_200_000_000},
            {"symbol": "CCC", "net_value": 8_100_000_000},
            {"symbol": "DDD", "net_value": 7_100_000_000},
            {"symbol": "EEE", "net_value": 6_100_000_000},
            {"symbol": "FFF", "net_value": 5_100_000_000},
            {"symbol": "GGG", "net_value": 4_100_000_000},
            {"symbol": "HHH", "net_value": -2_300_000_000},
            {"symbol": "HHH", "net_value": -1_200_000_000},
            {"symbol": "III", "net_value": -9_100_000_000},
            {"symbol": "JJJ", "net_value": -8_100_000_000},
            {"symbol": "KKK", "net_value": -7_100_000_000},
            {"symbol": "LLL", "net_value": -6_100_000_000},
            {"symbol": "MMM", "net_value": -5_100_000_000},
            {"symbol": "NNN", "net_value": -4_100_000_000},
        ]

        result = build_foreign_rankings(ranking_rows)

        self.assertEqual(result["top_buy"], [
            {"ticker": "BBB", "value": 9}, {"ticker": "CCC", "value": 8},
            {"ticker": "DDD", "value": 7}, {"ticker": "EEE", "value": 6},
            {"ticker": "FFF", "value": 5},
        ])
        self.assertEqual(result["top_sell"], [
            {"ticker": "III", "value": -9}, {"ticker": "JJJ", "value": -8},
            {"ticker": "KKK", "value": -7}, {"ticker": "LLL", "value": -6},
            {"ticker": "MMM", "value": -5},
        ])

    def test_build_market_week_normalizes_indices_and_foreign_flow(self):
        index_rows = {
            "VNINDEX": [("2026-08-21", 1788.78), ("2026-08-24", 1800.00), ("2026-08-28", 1832.12)],
            "VN30": [("2026-08-21", 1900.0), ("2026-08-24", 1910.0), ("2026-08-28", 1920.0)],
            "HNXINDEX": [("2026-08-21", 300.0), ("2026-08-24", 301.0), ("2026-08-28", 303.0)],
            "UPCOMINDEX": [("2026-08-21", 100.0), ("2026-08-24", 101.0), ("2026-08-28", 102.0)],
        }
        foreign_rows = [("2026-08-25", 276677170000), ("2026-08-26", -36997410000)]

        result = build_market_week(index_rows, [1000000000000, 2000000000000], foreign_rows, "2026-08-24")

        self.assertEqual(result["indices"][0], {"name": "VNINDEX", "close": "1,832.12", "change": "+43.34", "percent": "+2.42%"})
        self.assertEqual(result["trading_value"], "1,500")
        self.assertEqual(result["foreign_flow"], [{"date": "25/08", "value": 277}, {"date": "26/08", "value": -37}])


if __name__ == "__main__":
    unittest.main()
