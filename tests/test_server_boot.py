import os
import subprocess
import sys
import time
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ServerBootTests(unittest.TestCase):
    def test_server_starts_with_windows_cp1252_stdout(self):
        environment = {**os.environ, "PYTHONIOENCODING": "cp1252"}
        process = subprocess.Popen(
            [sys.executable, "server.py"],
            cwd=ROOT,
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        try:
            time.sleep(0.3)
            exit_code = process.poll()
            if exit_code is not None:
                _, stderr = process.communicate(timeout=1)
                self.fail(f"Server stopped with code {exit_code}: {stderr}")
        finally:
            process.terminate()
            process.communicate(timeout=3)


if __name__ == "__main__":
    unittest.main()
