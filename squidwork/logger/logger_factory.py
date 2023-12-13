from typing import Any


from squidwork.logger.logger_to_stdout import LoggerToStdout
from squidwork.logger.logger_to_logfile import LoggerToLogfile

class LoggerFactory:
    def __init__(self, log_output="stdout"):
        self.log_output = log_output
        
    def __call__(self):
        if self.log_output == "stdout":
            return LoggerToStdout()
        elif self.log_output == "logfile":
            return LoggerToLogfile()
        else:
            raise Exception("Invalid log_output")