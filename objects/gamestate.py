from enum import Enum

class GameState(Enum):
    QUIT = -1
    TITLE = 0
    START = 1
    CONFIG = 2
    DEBUG = 3