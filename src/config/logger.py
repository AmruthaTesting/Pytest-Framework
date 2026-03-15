import json
import logging
import os
import sys
from io import StringIO

import allure

_beautiful_json = dict(indent=2, ensure_ascii=False, sort_keys=True)

# Add custom log levels
logging.addLevelName(level=15, levelName="SUBDEBUG")
logging.addLevelName(level=5, levelName="TEST")

log_formatter = logging.Formatter(
    fmt="%(asctime)s [%(threadName)s] [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class CustomLogger(logging.Logger):
    test_log = StringIO()

    @staticmethod
    def format_message(message):
        return (
            json.dumps(message, **_beautiful_json)
            if isinstance(message, (dict, list, tuple))
            else str(message)
        )

    def subdebug(self, message, *args, **kwargs):
        if self.isEnabledFor(15):
            self._log(level=15, msg=message, args=args, **kwargs)

    def attach_debug(self, name, message):
        if self.isEnabledFor(10):
            allure.attach(
                self.format_message(message), name, allure.attachment_type.TEXT
            )

    def attach_subdebug(self, name, message):
        if self.isEnabledFor(15):
            allure.attach(
                self.format_message(message), name, allure.attachment_type.TEXT
            )

    def attach_info(self, name, message):
        if self.isEnabledFor(20):
            allure.attach(
                self.format_message(message), name, allure.attachment_type.TEXT
            )

    def attach_error(self, name, message):
        allure.attach(
            self.format_message(message), name, allure.attachment_type.TEXT
        )

    def add_handler(self, file_name, mode="a"):
        file_handler = logging.FileHandler(filename=file_name, mode=mode)
        file_handler.setFormatter(log_formatter)
        file_handler.setLevel(os.getenv("LOGGING_LEVEL_TO_CONSOLE", "INFO"))
        self.addHandler(file_handler)


def setup_logging():
    logger = CustomLogger("root")

    # Console handler — prints to terminal
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(os.getenv("LOGGING_LEVEL_TO_CONSOLE", "INFO"))
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)

    # StringIO handler — captured and attached to Allure report
    string_io = logging.StreamHandler(logger.test_log)
    string_io.setLevel(os.getenv("LOGGING_LEVEL", "INFO"))
    string_io.setFormatter(log_formatter)
    logger.addHandler(string_io)

    return logger


logger = setup_logging()
