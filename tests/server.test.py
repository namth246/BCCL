import json
import threading
import unittest
from urllib.request import urlopen

from server import create_server


class ServerTests(unittest.TestCase):
    def test_market_week_endpoint_rejects_invalid_date_range(self):
        server = create_server(0)
        thread = threading.Thread(target=server.handle_request)
        thread.start()
        try:
            with self.assertRaises(Exception) as error:
                urlopen(f"http://127.0.0.1:{server.server_port}/api/market-week?start=bad&end=2026-08-28")
            self.assertIn("HTTP Error 400", str(error.exception))
        finally:
            thread.join(timeout=2)
            server.server_close()


if __name__ == "__main__":
    unittest.main()
