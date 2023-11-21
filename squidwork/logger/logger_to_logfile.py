import logging
from sys import stderr
from datetime import datetime
from pathlib import Path

from .logger import Logger

class LoggerToLogfile(Logger):
    def __init__(self, cache_dir):
        super().__init__()
        self.cache_dir = cache_dir
        self.logfile = Path(f"{self.cache_dir}/squidwork.log")
        self.backupOldRunLogfile()

        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s %(levelname)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            filename=self.logfile
        )

    def backupOldRunLogfile(self):
        curr_date = datetime.now().strftime("%S-%M-%H_%d-%m-%Y")
        logfile_backup = Path(f"{self.logfile}_{curr_date}.bak")
        try:
            if self.logfile.exists():
                with open(self.logfile, 'r') as old_run_logfile:
                    with open(f"{logfile_backup}", 'a') as logfile_bakckup_handle:
                        logfile_bakckup_handle.write(old_run_logfile.read())
                self.logfile.unlink()
        except Exception as e:
            raise(f"[x] Error backing up {self.logfile} to {logfile_backup}: {e}k\n")

