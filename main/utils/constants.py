from os.path import dirname, realpath
from enum import Enum

APP_DEBUG = True
APP_HOST = "0.0.0.0"
APP_PORT = 5016
APP_ENGINE_NAME = "ParsPack"

# Use dirname twice because the file is inside the utils folder
APP_BASE_DIR = dirname(dirname(realpath(__file__)))
REPORT_PATH = f"{APP_BASE_DIR}/results/"


# Regular expression for IPv4 addresses
IPV4_REGEX = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
# Regular expression for IPv6 addresses
IPV6_REGEX = r"^\[?([a-fA-F0-9:]+)\]?$"


class CeleryStatus(Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"


class PatrwolStatus(object):
    FINISHED = "FINISHED"
    SCANNING = "SCANNING"
    UNKNOWN = "UNKNOWN"
    ERROR = "ERROR"
