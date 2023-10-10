import logging
from customlogformatter import CustomLogFormatter

# How To Use Logging In Multiple Modules?
# https://betterstack.com/community/questions/how-to-use-logging-in-multiple-modules/

logger = logging

# formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(CustomLogFormatter())

logging.basicConfig(
    level=logging.INFO,
    handlers=[handler]
)