import unittest
from unittest.mock import patch, MagicMock
from optimization.local_optimizer import LocalOptimizer


class TestLocalOptimizer(unittest.TestCase):
    def setUp(self):
        self.config = MagicMock(
            x0=0, y0=0, x_min=-10, x_max=10, timeout=30, log_file="test.log"
        )
        self.optimizer = LocalOptimizer(self.config)

    def test_local_optimization_with_mock(self):
        with patch("util.external_runner.run_external_program", return_value=42.0):
            result = self.optimizer.optimize()
            self.assertIn("success", result.message.lower())
