import unittest
from unittest.mock import patch, MagicMock
import logging
import subprocess
from util.external_runner import run_external_program


class MockConfig:
    """Mock configuration class to mimic the behavior of the actual Config class."""

    def __init__(self):
        self.log_file = "mock.log"
        self.x_min = -10
        self.x_max = 10
        self.timeout = 30
        self.log_file = "test.log"

    def setup_logging(self):
        """Mock _setup_logging method."""
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

class TestExternalRunnerWithMockConfig(unittest.TestCase):
    def setUp(self):
        """Set up the test with a mock configuration."""
        self.mock_config = MockConfig()

    @patch("subprocess.run")
    def test_valid_run(self, mock_subprocess):
        """Test external runner with valid output."""
        mock_subprocess.return_value = MagicMock(stdout="42.0", returncode=0)
        result = run_external_program(1, 2, self.mock_config)
        self.assertEqual(result, 42.0)

    @patch("subprocess.run")
    def test_timeout(self, mock_subprocess):
        """Test external runner when a timeout occurs."""
        mock_subprocess.side_effect = subprocess.TimeoutExpired(cmd="cmd", timeout=self.mock_config.timeout)
        result = run_external_program(1, 2, self.mock_config)
        self.assertEqual(result, float('inf'))

    @patch("subprocess.run")
    def test_non_zero_exit(self, mock_subprocess):
        """Test external runner when a subprocess exits with an error."""
        mock_subprocess.return_value = MagicMock(stdout="", returncode=1, stderr="Error")
        result = run_external_program(1, 2, self.mock_config)
        self.assertEqual(result, float('inf'))
