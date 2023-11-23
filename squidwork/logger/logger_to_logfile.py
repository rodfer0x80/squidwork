import logging, os
from datetime import datetime
from pathlib import Path

from .logger import Logger

class LoggerToLogfile(Logger):
    def __init__(self, cache_dir):
        super().__init__()
        self.cache_dir = cache_dir
        curr_date = datetime.now().strftime("%H-%M-%S_%d-%m-%Y")
        self.logfile = Path(os.path.join(self.cache_dir, f"squidwork_{curr_date}.log"))
        #self.backupOldRunLogfile()

        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s %(levelname)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            filename=self.logfile
        )