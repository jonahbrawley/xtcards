from enum import Enum

class GameState(Enum):
    SCAN_AI_HAND = 0        #  AI's hand at the beginning of the round
    POST_AI_BETS = 1

    SCAN_FLOP = 2           #  scan 3 cards
    POST_FLOP_BETS = 3

    SCAN_TURN = 4           #  scan 1 card
    POST_TURN_BETS = 5

    SCAN_RIVER = 6          #  scan 1 card - aka the final 'flip'
    FINAL_BETS = 7

    SCAN_PLAYER_HAND = 8    #  player's hand at end to determine who wins
    
    END_ROUND = 9           #  show results of round
    END_SCREEN = 10         # show results of entire game