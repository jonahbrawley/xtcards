from game_logic.deck import Deck
from game_logic.card_ranker import CardRanker
from game_logic.player import Player
from game_logic.pot import TempPot
from game_logic.poker_agent import predict_ai_move
import random
from enum import Enum
from objects.gamestate import GameState


class GameInstance:
  class StartResponse(Enum):
    successful = 0
    not_enough_players = 1
    game_in_progress = 2

  class GameRound(Enum):
    PREFLOP = 0
    FLOP = 1
    TURN = 2
    RIVER = 3
    END = 4

  
  USE_PHYSICAL_DECK = True
  SMALL_BLIND = 5
  BIG_BLIND = 10

  def __init__(self, players):
    self.players = players
    self.game_active = False
    self.dealer_pos = random.randint(0, len(self.players))
    self.curr_pos = 0

  # Check which players can start a new game and return that number
  def ready_up_players(self):
    ready_players = 0
    for player in self.players:
      if player.chips == 0:
        player.last_action = "out"
      else:
        player.last_action = "wait"
        ready_players += 1
    return ready_players

  # Given a current player position, get the next player's
  # position who is still active (chips > 0 and necessary last_action)
  # THIS METHOD SHOULD NOT BE REACHABLE IF THERE ARE NO NEXT ACTIVE PLAYERS
  # THERE SHOULD BE PRIOR CHECKS IN PLACE FOR `self.is_round_over()` TO END ROUND
  def get_next_pos(self, pos):
    n_players = len(self.players)
    player_inactive = True
    while player_inactive:
      pos = (pos + 1) % n_players
      player_inactive = self.players[pos].chips <= 0 or self.players[pos].last_action in ["pending_out", "out", "fold", "all_in"]
    return pos

  def increment_curr_pos(self):
    self.curr_pos = self.get_next_pos(self.curr_pos)
    return self.curr_pos

  def increment_dealer_pos(self):
    self.dealer_pos = self.get_next_pos(self.dealer_pos)
    return self.dealer_pos

  def is_curr_pos_at_ai(self):
    return self.players[self.curr_pos].is_ai
  
  def get_min_required_bet(self, player=None):
    if not player:
      player = self.players[self.curr_pos]
    return self.tmp_pot.highest_bet() - self.tmp_pot.bets[player.id]


  # setup all variables for a new game state
  def start_game(self):
    # Don't start a new game if one is in progress already
    if self.game_active:
      print("Error: Cannot start a new game because a game is in progress.")
      return GameState.ERROR_STATE

    # Check if enough players have chips to start a new gme
    if self.ready_up_players() < 2:
      print("Error: Cannot start a new game because not enough players have chips.")
      return GameState.ERROR_STATE

    # Setup all variables
    self.deck = Deck()

    # keep track of a single pot that can be split into side pots
    # NOTE: at the end of the game, this pot will be forced into side pots
    # because `side_pots` is coupled with chip winnings distribution
    self.tmp_pot = TempPot(self.players)

    # keep track of all the side pots that break off of the tmp pot
    # store main & side pots for winnings distribution
    self.side_pots = []

    self.round = self.GameRound.PREFLOP
    self.community_cards = [Deck.UNKNOWN_CARD_SYMBOL for _ in range(5)]
    self.increment_dealer_pos()
    self.curr_pos = self.dealer_pos # game starts from dealer position
    self.game_active = True

    # If a physical deck is not being used, deal all the cards to the players
    if not GameInstance.USE_PHYSICAL_DECK:
      for player in self.players:
        if player.cards is None:
          player.pull_cards(self.deck)
    
    return GameState.SCAN_AI_HAND

  def await_player_action(self, player):
    print(GameInstance.divider("Player Action"))
    print(player)

    p_action = None

    while p_action is None:
      p_action = input(f"Bet requirement: {self.tmp_pot.highest_bet() - self.tmp_pot.bets[player.id]}\nMake your move (fold, call, raise, all_in):")
      if p_action not in ["fold", "call", "raise", "all_in"]:
        p_action = None

    if p_action != "raise":
      return p_action, 0

    p_bet = None

    while p_bet is None:
      try:
        p_bet = int(input("What is your bet?"))
        print("Value input: " + p_bet)
      except:
        print("Error: Please enter a number.")
      if p_bet < 0 or p_bet > player.chips:
        p_bet = None

    return p_action, p_bet

  def execute_player_action(self, player, action, bet_amount):
    min_required_bet = self.get_min_required_bet(player)
    print(f"min_required_bet = {min_required_bet}")

    if action == "fold":
      bet_amount = 0

    elif action == "all_in":
      bet_amount = player.chips

    elif action == "call":
      bet_amount = min(min_required_bet, player.chips)
      if bet_amount == player.chips:
        action = "all_in"
      elif bet_amount < min_required_bet:
        return False

    elif action == "raise":
      bet_amount = min_required_bet + bet_amount
      if bet_amount == player.chips:
        action = "all_in"
      elif bet_amount == min_required_bet:
        action = "call"
      elif bet_amount > player.chips:
        return False
      elif bet_amount < min_required_bet:
        return False
    
    elif action == "blind":
      if bet_amount == player.chips:
        action = "all_in"
      else:
        action = "wait"
    
    else:
      return False

    player.last_action = action
    self.tmp_pot.add_to_pot(player.id, bet_amount)
    player.chips -= bet_amount
    player.curr_bet = self.tmp_pot.bets[player.id]

    return True

  def is_awaiting_preflop(self):
    return self.round == self.GameRound.PREFLOP and self.tmp_pot.sum_bets() == 0

  # Initiate the next game step
  # E.g. start round, reveal community card, next player move, etc.
  def step(self, p_action=None, p_bet=None):
      '''
      Initiate the next game step (e.g. start round, player move, etc.)
      Returns: GameState -- next game state value after step method is completed
      '''
      if not self.game_active or self.round == self.GameRound.END:
        print("Error: Cannot step to next game move because game is not in progress.")
        return GameState.ERROR_STATE

      # Detect start of game: round == preflop, pot == 0
      if self.is_awaiting_preflop():
        print("(GameInstance) Applying small and big blinds")
        # if there are only 2 players, player with dealer chip is also small blind
        # otherwise small blind is the player after the dealer chip
        if len(self.players_that_can_do_action()) > 2:
          self.increment_curr_pos()

        p_sm = self.players[self.curr_pos]
        self.execute_player_action(p_sm, "blind", min(p_sm.chips, GameInstance.SMALL_BLIND))
        self.increment_curr_pos()

        p_b = self.players[self.curr_pos]
        self.execute_player_action(p_b, "blind", min(p_b.chips, GameInstance.BIG_BLIND))
        self.increment_curr_pos()
        return GameState.PREFLOP_BETS # this is the next state the game should look at
      else:
        # If a play should not take place, end round immediately
        if self.is_round_over():
          next_game_state = self.end_round()
          return next_game_state
          # return the next GameState state that the game should proceed with


        # individual player move
        curr_player = self.players[self.curr_pos]

        valid_bet = self.execute_player_action(curr_player, p_action, p_bet)
        if not valid_bet:
          print("Error: Bet amount was not valid")
          return GameState.ERROR_STATE


      # Check and handle if the round shound be over
      if self.is_round_over():
        print("end of round")
        next_game_state = self.end_round()
        return next_game_state

      # round is not over, move to next player
      else:
        self.increment_curr_pos()

      print("Reached end of step() method and no GameState value returned. Assuming betting continues for this round.")
      return GameState.UNCHANGED_STATE

  # OR n-1 players are either "out" or "fold", one person wins
  def is_round_over(self):
    # check if only one player is not out
    out_cnt = 0
    for p in self.players:
      if p.last_action in ["pending_out", "out", "fold"]:
        out_cnt += 1
    if out_cnt == len(self.players) - 1:
      return True

    # check if everyone has placed the minimum required bet and is not out
    highest_bet = self.tmp_pot.highest_bet()
    cnt = 0
    for p in self.players:
      if p.last_action == "wait":
        return False
      if not p.can_do_action() or (p.curr_bet == highest_bet and p.can_do_action()):
        cnt += 1
    # print(f"round over: {cnt == len(self.players)}")
    return cnt == len(self.players)

  # If a round begins where only one player has the ability place a bet, the game should end
  def should_round_begin(self):
    cnt = 0
    for p in self.players:
      if p.last_action == "wait":
        cnt += 1
      if cnt > 1:
        return True
    return False

  # update board when a round is over
  # NOTE: this is NOT the end of the game, only the end of the current betting round
  def end_round(self):
    round_is_over = True
    while round_is_over:
      # default all players action to wait at start of round
      for player in self.players:
        if player.last_action == "all_in":
          player.last_action = "pot_committed"

        if player.last_action != "pending_out" and player.last_action != "out" and player.last_action != "pot_committed" and player.last_action != "fold":
          player.last_action = "wait"
          player.curr_bet = 0

      if self.round == self.GameRound.PREFLOP:
        print("Flop")
        self.round = self.GameRound.FLOP
      elif self.round == self.GameRound.FLOP:
        print("Turn")
        self.round = self.GameRound.TURN
      elif self.round == self.GameRound.TURN:
        print("River")
        self.round = self.GameRound.RIVER
      elif self.round == self.GameRound.RIVER:
        print("End")
        self.round = self.GameRound.END
        return GameState.SCAN_PLAYER_HAND # End of game, next GameState should be scanning player cards

      # this `else` shouldn't be reached unless there is an error with the self.round field
      else:
        print(f"Error: could not proceed to next round from GameRound='{self.round}'")
        return GameState.ERROR_STATE

      # split out sidepots
      self.side_pots += self.tmp_pot.to_sidepots()
      # curr_pot.to_sidepots() naturally returns player bets to 0
      round_is_over = self.is_round_over()

      if not self.should_round_begin():
        round_is_over = True

    # Move curr_pos to next active player after dealer if
    self.curr_pos = self.get_next_pos(self.dealer_pos)

    # Game has not ended yet, return next GameState that game should do
    if self.round == self.GameRound.FLOP:
      return GameState.SCAN_FLOP
    elif self.round == self.GameRound.TURN:
      return GameState.SCAN_TURN
    elif self.round == self.GameRound.RIVER:
      return GameState.SCAN_RIVER
    elif self.round == self.GameRound.END:
      return GameState.SCAN_PLAYER_HAND
    
    print("Reached end of end_round() method and no GameState is returned. There may be a bug.")
    return GameState.ERROR_STATE


  # Called after river betting & cards are revealed
  # Player cards must be scanned before this method is called
  # (e.g. GameState.SCAN_PLAYER_HAND -> GameState.END_ROUND)
  def end_game(self):
    # split into pots one last time
    self.side_pots += self.tmp_pot.to_sidepots()

    # rank and calculate winnings for players based on cards
    rankings, winnings = CardRanker.rank_and_calculate_winnings(self.players, self.community_cards, self.side_pots)

    # distribute winnings
    for player in self.players:
      if player.id in winnings.keys():
        player.chips += winnings[player.id]

    # show off winning amounts
    print("WINNINGS:")
    print(winnings)

    # for each player with no chips, set player.last_action to "out"
    for p in self.players:
      if p.chips == 0 and p.last_action != "out":
        p.last_action = "pending_out"
        print(f"Player Out: {p.name}")
    self.game_active = False

    return rankings, winnings


  def players_that_can_do_action(self):
    res = []
    for player in self.players:
      if player.can_do_action():
        res.append(player)
    return res

  def get_total_pot_value(self):
    # current round pot value
    pot_round_value = self.tmp_pot.sum_bets()

    # total game pot value
    pot_game_value = pot_round_value
    for pot in self.side_pots:
      pot_game_value += pot.sum_bets()

    return pot_game_value

  def get_state_ai(self, pos=None):
    '''
    data to add to dictionary:
    - river state/round name
    - total game pot value
    - current round pot
    - opponents' last actions, current bets, chip counts (only who is still playing & not including current pos)
    - community cards
    - ai's cards
    - ai's last action
    - ai's current bet amount
    '''
    print("Generating a json object for the AI model at curr_pos")
    if pos == None:
      pos = self.curr_pos

    river_state = self.round.name

    # current round pot value
    pot_round_value = self.tmp_pot.sum_bets()

    # total game pot value
    pot_game_value = pot_round_value
    for pot in self.side_pots:
      pot_game_value += pot.sum_bets()

    community_cards = self.community_cards
    ai_instance = self.players[pos]
    ai_cards = ai_instance.cards
    ai_last_action = ai_instance.last_action
    ai_curr_bet = ai_instance.curr_bet

    # opponents must be NOT 'out' and NOT be the current ai player
    opponents_data = []
    for opponent in self.players:
      if opponent.id != pos and opponent.last_action != 'out':
        opponent_obj = {
          "last_action" : opponent.last_action,
          "curr_bet" : opponent.curr_bet,
          "chips" : opponent.chips
        }
        opponents_data.append(opponent_obj)

    res_dict = {
      "river_state" : river_state,
      "pot_round" : pot_round_value,
      "pot_game" : pot_game_value,
      "community_cards" : community_cards,
      "ai_cards" : ai_cards,
      "ai_last_action" : ai_last_action,
      "ai_curr_bet" : ai_curr_bet,
      "opponents" : opponents_data
    }

    return res_dict

  def divider(s):
    return "\n-------------------- " + s + " --------------------\n\n"

  def __str__(self):


    res = "\n\n\n"

    res += GameInstance.divider("General State")
    res += f"Round: {self.round}\n"
    res += f"Community Cards: {self.community_cards}\n"
    res += f"Dealer Position: {self.dealer_pos}\n"
    res += f"Current Position: {self.curr_pos}\n"
    res += f"Current Player: {self.players[self.curr_pos].name}\n"

    res += GameInstance.divider(f"Players ({len(self.players)})")
    for player in self.players:
      res += f"ID{player.id}, chips:{player.chips}, cards:{player.cards}, last_action:{player.last_action}\n"

    res += GameInstance.divider("Current Pot")
    for key, value in self.tmp_pot.bets.items():
      res += f"{key}:${value}\t"
    res += GameInstance.divider("Final Pots")
    for i, pot in enumerate(self.side_pots):
      for key, value in pot.bets.items():
        res += f"{key}:${value}\t"

    return res

# Sample code previously used in game demo

# players = [
#   Player("Bill", is_ai=False, chips=100, cards=["AH", "AS"], id=0), 
#   Player("John", is_ai=True, chips=200, cards=["KC", "8H"], id=1), 
#   Player("Sam", is_ai=False, chips=300, cards=["2D", "2C"], id=2)
#   ]

# community_cards = ['2H', '2D', '8C', '6C', '7H']

# instance = GameInstance(players)
# instance.start_game()
# instance.community_cards = community_cards

# while True:
#   while instance.game_active:
#     # send out small and big blind
#     if instance.is_awaiting_preflop():
#       print(instance.step().name)
#     # execute a player turn & update round/cards if necessary
#     else:
#       next_state = None
#       if instance.is_curr_pos_at_ai():
#         print("AI response")
#         ai_state = instance.get_state_ai()
#         p_action = predict_ai_move(ai_state)
#         next_state = instance.step(p_action)
#       else:
#         print("Not AI response")
#         p_action = input("Action:\n")
#         p_bet = None
#         if p_action.lower() == "raise":
#           p_bet = int(input("Bet:\n"))
#         next_state = instance.step(p_action, p_bet)
        
#       if next_state == GameState.SCAN_PLAYER_HAND:
#         print(instance.end_game())

#     print(instance.players[instance.curr_pos], instance.curr_pos)
#     if instance.game_active:
#       print(instance)


#   response = instance.start_game()
#   if response == GameState.ERROR_STATE:
#     break

# for player in players:
#   print(player)