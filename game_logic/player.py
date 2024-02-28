class Player:
  __ids = [] # store all player ids privately
  def __init__(self, name, is_ai, id, chips=1000, cards=None):
    self.id = id
    self.name = name
    self.chips = chips
    # NOTE: pending_out means the game ended and the player will be out on the next round
    self.last_action = None # wait, fold, call, raise, all_in, pot_committed, out
    self.curr_bet = 0
    self.cards = cards
    self.is_ai = is_ai

  def pull_cards(self, deck):
    self.cards = [deck.pull(), deck.pull()]

  def can_do_action(self):
    return self.chips > 0 and self.last_action not in ["all_in", "fold", "pending_out", "out"]

  def __str__(self):
    return (
        f"Player {self.id}: {self.name}\n" +
        f"\tchips: {self.chips}\n" +
        f"\taction: {self.last_action}\n" +
        f"\tcurrent_bet: {self.curr_bet}\n" +
        f"\tcards: {self.cards}\n"
        )