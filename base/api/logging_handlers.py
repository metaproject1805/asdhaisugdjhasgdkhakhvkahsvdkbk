# logging_handlers.py

import logging

class RequestLoggingHandler(logging.Handler):
    def __init__(self, file_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_path = file_path

    def emit(self, record):
        log_entry = self.format(record)
        with open(self.file_path, 'a') as log_file:
            log_file.write(log_entry + '\n')
