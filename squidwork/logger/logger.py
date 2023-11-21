import logging

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
