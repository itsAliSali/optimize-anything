import unittest
from util.config_loader import Config
import os


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.valid_config = "test_config_valid.ini"
        self.invalid_config = "test_config_invalid.ini"
        
        # Create valid test config
        with open(self.valid_config, "w") as f:
            f.write("""
                [Optimization]
                log_file = test.log
                pop_size = 5
                max_generations = 10
                seed = 1
                timeout = 30
                method = global

                [Bounds]
                x_min = -10
                x_max = 10

                [InitialGuess]
                x0 = 0
                y0 = 0
            """)

        # Create invalid test config
        with open(self.invalid_config, "w") as f:
            f.write("invalid_content")

    def tearDown(self):
        os.remove(self.valid_config)
        os.remove(self.invalid_config)

    def test_valid_config(self):
        config = Config(self.valid_config)
        self.assertEqual(config.x0, 0)
        self.assertEqual(config.timeout, 30)
        self.assertEqual(config.method, "global")

    def test_invalid_config(self):
        with self.assertRaises(Exception):
            Config(self.invalid_config)
