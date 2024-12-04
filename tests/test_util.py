import unittest
from unittest.mock import patch
import time
import re
from util.timer_decorator import time_function


class TestTimer(unittest.TestCase):
    def test_timer_decorator(self):
        @time_function("Test function")
        def sample_function():
            time.sleep(1.07)
            return "done"

        with patch("logging.info") as mock_log:
            result = sample_function()
            self.assertEqual(result, "done")
            
            logged_message = mock_log.call_args[0][0]
            match = re.search(r"Test function: (\d+\.\d+) seconds", logged_message)
            self.assertIsNotNone(match, "No timing information found in log message.")

            elapsed_time = float(match.group(1))
            
            # Assert the elapsed time is within a reasonable range
            self.assertGreaterEqual(elapsed_time, 1.0)
            self.assertLessEqual(elapsed_time, 1.5)
