from enum import Enum

class CameraState(Enum):
    SCAN_AI_HAND = 0        #  AI's hand at the beginning of the round
    SCAN_FLOP = 1           #  3 cards
    SCAN_TURN = 2           #  1 card
    SCAN_RIVER = 3          #  1 card - final 'flip' before reveal
    SCAN_PLAYER_HAND = 4    #  player's hand at end to determine who wins