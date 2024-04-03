from enum import Enum

class ScreenState(Enum):
    QUIT = -1
    TITLE = 0
    START = 1
    LOAD = 2
    DEBUG = 3