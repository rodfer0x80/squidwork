import logging, os
from datetime import datetime
from pathlib import Path

from .logger import Logger
#from http.server import BaseHTTPRequestHandler, HTTPServer

class LoggerToLogfile(Logger):
    def __init__(self, cache_dir):
        super().__init__()
        self.cache_dir = cache_dir
        self.logfile = Path(os.path.join(self.cache_dir, "squidwork.log"))
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
        if self.logfile.exists():
            self.backupLogfile(logfile_backup)
    
    def backupLogfile(self, logfile_backup: Path):
        try:
            with open(self.logfile, 'r') as old_run_logfile:
                with open(f"{logfile_backup}", 'a') as logfile_bakckup_handle:
                    logfile_bakckup_handle.write(old_run_logfile.read())
            self.logfile.unlink()
        except Exception as e:
            raise(f"[x] Error backing up {self.logfile} to {logfile_backup}: {e}k\n")


    # TODO: add logging to browser so we can have a lot of bots and read logs from /logger/$n

    # def get_log_content(self):
    #     try:
    #         with open(self.logfile, 'r') as file:
    #             return file.read()
    #     except FileNotFoundError:
    #         return 'Logfile not found'
#  class LogFileRequestHandler(BaseHTTPRequestHandler):
#     logger_instance = LoggerToLogfile('/path/to/cache')  # Update with your cache_dir path

#     def do_GET(self):
#         self.send_response(200)
#         self.send_header('Content-type', 'text/plain')
#         self.end_headers()

#         if self.path == '/logfile':
#             content = self.logger_instance.get_log_content()
#             self.wfile.write(content.encode())
#         else:
#             self.wfile.write(b'Invalid path')

# def run_server(port=8080):
#     server_address = ('', port)
#     httpd = HTTPServer(server_address, LogFileRequestHandler)
#     print(f'Server running on port {port}')
#     httpd.serve_forever()

# if __name__ == '__main__':
#     LoggerToLogfile('/path/to/cache').start()  # Start the logger
#     run_server()