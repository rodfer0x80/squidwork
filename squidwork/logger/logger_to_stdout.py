import logging
from .logger import Logger

class LoggerToStdout(Logger):
    def __init__(self):
        super().__init__()
        logging.basicConfig(level=logging.DEBUG)
    
    # implement methods to stdout
