import logging, os
from datetime import datetime
from pathlib import Path

class Logger:
    def __init__(self):
        return None

    def log(self, msg: str) -> int:
        return self.info(msg)

    def debug(msg: str) -> int:
        try:
            logging.debug(f"{msg}")
            return 0
        except Exception as e:
            raise(f"Error: {e}")

    def info(self, msg: str) -> int:
        try:
            logging.info(f"{msg}")
            return 0
        except Exception as e:
            raise(f"Error: {e}\n")

    def warning(self, msg: str) -> int:
        try:
            logging.warning(f"{msg}")
            return 0
        except Exception as e:
            raise(f"Error: {e}")

    def error(self, msg: str) -> int:
        try:
            logging.error(f"{msg}")
            return 0
        except Exception as e:
            raise(f"Error: {e}")

    def critical(self, msg: str) -> int:
        try:
            logging.critical(f"{msg}")
            return 0
        except Exception as e:
            raise(f"Error: {e}\n")


class LoggerToLogfile(Logger):
    def __init__(self, cache_dir):
        super().__init__()

        self.cache_dir = cache_dir

        curr_date = datetime.now().strftime("%H-%M-%S_%d-%m-%Y")
        self.logfile = Path(os.path.join(self.cache_dir, f"squidwork_{curr_date}.log"))

        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s %(levelname)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            filename=self.logfile
        )