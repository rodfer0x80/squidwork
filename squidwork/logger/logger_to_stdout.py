class LoggerToStdout:
    def __init__(self):
        pass 

    def log(self, msg: str):
        self.debug(msg)

    def debug(self, msg: str):
        print(f"[DEBUG]: {msg}")

    def info(self, msg: str):
        print(f"[INFO]: {msg}")

    def warning(self, msg: str):
        print(f"[WARNING]: {msg}")

    def error(self, msg: str):
        print(f"[ERROR]: {msg}")

    def critical(self, msg: str):
        print(f"[CRITICAL]: {msg}")