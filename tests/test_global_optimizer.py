import unittest
from unittest.mock import patch
import numpy as np
from optimization.global_optimizer import GlobalOptimizer, ExternalProblem


class TestGlobalOptimizer(unittest.TestCase):
    def setUp(self):
        # Mock configuration for testing
        self.config = type(
            "ConfigMock",
            (object,),
            {
                "x_min": -10,
                "x_max": 10,
                "max_generations": 3,
                "pop_size": 5,
                "timeout": 30,
                "log_file": "test.log",
                "seed": 1,
            },
        )()
        self.optimizer = GlobalOptimizer(self.config)

    @patch("optimization.global_optimizer.ExternalProblem._evaluate")
    def test_global_optimization_with_mock(self, mock_evaluate):
        import warnings
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # Mock the fitness values for the population
        def mock_evaluate_population(_, out):
            out["F"] = np.array([42.0] * self.config.pop_size)  # Simulated fitness values
        mock_evaluate.side_effect = mock_evaluate_population

        result = self.optimizer.optimize()
        self.assertEqual(len(result.X), 2)  # Check if solution has 2 variables
        self.assertEqual(result.F, 42.0)  # Verify mocked fitness value

