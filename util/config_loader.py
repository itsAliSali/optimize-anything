import configparser
import logging


class Config:
    def __init__(self, config_file="config.ini"):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

        self.log_file = self.config["Optimization"].get("log_file", "optimization.log")
        self.pop_size = self.config["Optimization"].getint("pop_size", 50)
        self.max_generations = self.config["Optimization"].getint("max_generations", 10)
        self.seed = self.config["Optimization"].getint("seed", 1)
        self.timeout = self.config["Optimization"].getint("timeout", 30)
        self.method = self.config["Optimization"].get("method", "local").lower()
        self.x_min = self.config["Bounds"].getfloat("x_min", -512)
        self.x_max = self.config["Bounds"].getfloat("x_max", 512)
        self.x0 = self.config["InitialGuess"].getfloat("x0", 0)
        self.y0 = self.config["InitialGuess"].getfloat("y0", 0)

        self._setup_logging()
        logging.info("Configuration and logging initialized.")

    def _setup_logging(self):
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def __repr__(self):
        return (
            f"Config(log_file={self.log_file}, pop_size={self.pop_size}, "
            f"max_generations={self.max_generations}, seed={self.seed}, "
            f"timeout={self.timeout}, x_min={self.x_min}, x_max={self.x_max}, "
            f"x0={self.x0}, y0={self.y0})"
        )

    def setup_logging(self):
        self._setup_logging()