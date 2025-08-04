import sys
from colorama import just_fix_windows_console
from typing import TextIO, final, override
import logging

# Ensure that Windows shells can properly parse the ANSI codes
just_fix_windows_console()


@final
class TermFormat:
    """
    An enum-like class that encapsulates various ANSI values into a class.
    """

    # Standard Colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    PURPLE = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Intense Colors
    BLACK_INT = "\033[90m"
    RED_INT = "\033[91m"
    GREEN_INT = "\033[92m"
    YELLOW_INT = "\033[93m"
    BLUE_INT = "\033[94m"
    PURPLE_INT = "\033[95m"
    CYAN_INT = "\033[96m"
    WHITE_INT = "\033[97m"

    # Styling
    HEADER = "\033[95m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    RESET = "\033[0m"


class Formatter(logging.Formatter):

    COLOR_LOOKUP: dict[int, str] = {
        logging.DEBUG: TermFormat.PURPLE_INT,
        logging.INFO: TermFormat.WHITE,
        logging.WARNING: TermFormat.YELLOW_INT,
        logging.ERROR: TermFormat.RED_INT,
        logging.CRITICAL: TermFormat.RED_INT + TermFormat.BOLD,
    }

    @override
    def format(self, record: logging.LogRecord) -> str:
        levelname = record.levelno
        color = self.COLOR_LOOKUP[levelname]
        message = super().format(record)
        return f"{color}{message}"


class Logger(logging.Logger):
    """
    <SINGLETON>

    This class encapsulates methods that can be used to print information to
    the console output, allowing the program to communicate with the user. It
    builds on the native "logging" logger by being able to provide formatted
    output using ANSI codes. In addition, it stores the configurations needed
    to set everything up.
    """

    fmt: str = "[%(name)s] [%(levelname)s] - %(message)s"
    
    def __init__(self, name: str) -> None:
        super().__init__(name)

        handler: logging.StreamHandler[TextIO] = logging.StreamHandler(sys.stdout)
        formatter: Formatter = Formatter(self.fmt)
        handler.setFormatter(formatter)

        self.addHandler(handler)
        # Change this to the value you want
        self.setLevel(logging.INFO)

logging.setLoggerClass(Logger)
