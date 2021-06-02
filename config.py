import logging
import datetime as dt

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
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
logger.addHandler(handler)

# Fixed date and time for the start.
START_DATE = dt.datetime(2021, 6, 1, 23, 59, 59)
# Fixed RA and DEC for the above mentioned START_DATE.
FIX_RA = [22, 46, 54]
FIX_DEC = [-13, 27, 21]
FIX_RA_IN_SEC = FIX_RA[0] * 3600 + FIX_RA[1] * 60 + FIX_RA[0]
FIX_DEC_IN_SEC = FIX_DEC[0] * 3600 + FIX_DEC[1] * 60 + FIX_DEC[0]
# The average change of the Moon RA (in seconds) within one second.
AV_CHANGE_OF_M_RA_S = 0.036
# The average change of the Moon DEC (in seconds) within one second.
AV_CHANGE_OF_M_DEC_S = 0.185
