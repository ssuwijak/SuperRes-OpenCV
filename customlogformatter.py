import logging

# https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output

class ColorCodes:
    # ANSI escape code
    # https://en.wikipedia.org/wiki/ANSI_escape_code
    # https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797

    grey = "\x1b[38;21m"
    green = "\x1b[1;32m"
    yellow = "\x1b[33m"
    yellow_doubleunderline = "\x1b[33;21m"
    orange = "\x1b[38;5;208m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    bold_white_on_red = "\x1b[1;37;41m"
    blue = "\x1b[1;34m"
    light_blue = "\x1b[1;36m"
    purple = "\x1b[1;35m"
    reset = "\x1b[0m"

class CustomLogFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(levelname)-8s - %(name)-10s - %(message)s (%(filename)s:line %(lineno)d)"

    FORMATS_0 = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    FORMATS = {
        logging.DEBUG: ColorCodes.grey + format + ColorCodes.reset,
        logging.INFO: ColorCodes.green + format + ColorCodes.reset,
        logging.WARNING: ColorCodes.yellow + format + ColorCodes.reset,
        logging.ERROR: ColorCodes.red + format + ColorCodes.reset,
        logging.CRITICAL: ColorCodes.bold_white_on_red + format + ColorCodes.reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)