import logging

# Global constants
IP = "localhost"
PORT = 5050
SLEEP_TIME = 10

# Global variables
USERS = set()

# Info and error logger with handler.
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s: %(asctime)s: %(name)s: %(message)s')

handler = logging.FileHandler("users.log", mode="w")
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)

logger.addHandler(handler)
