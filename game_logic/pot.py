class Pot:
  def __init__(self, bets=None):
    if bets is None:
      self.bets = {}
    else:
      self.bets = bets

  def add_to_pot(self, player_id, chips):
    self.bets[player_id] += chips

  def sum_bets(self):
    return sum(self.bets.values())

  def highest_bet(self):
    if len(self.bets) == 0:
      return 0
    return max(self.bets.values())

  def __str__(self):
    res = f"Pot ${self.sum_bets()} \nPlayers:\n"
    for k, v in self.bets.items():
      res += f"\tPlayer{k}: ${v}\n"
    return res

class TempPot(Pot):
  def __init__(self, players):
    bets = {}
    for player in players:
      bets[player.id] = 0
    super().__init__(bets)

  def to_sidepots(self, end_of_game=False):
    # Create the side pots
    res_pots = []
    while True:
      # determine the next side pot
      curr_pot = {}
      smallest_bet = float('inf')

      # find the smallest bet to make up the next side pot
      for value in self.bets.values():
        if value > 0:
          smallest_bet = min(smallest_bet, value)

      # if remaining bets are all $0, no more side pots are necessary
      if smallest_bet == float('inf'):
        break

      # add smallest bet into current side pot for each valid participant
      for key, value in self.bets.items():
        if value > 0:
          self.bets[key] -= smallest_bet
          curr_pot[key] = smallest_bet

      # A key-value pair for this pot has been made and values in `bets` have
      # subtracted the smallest bet for this pot.
      # Add the current subpot to the dictionary and proceed to the next one
      res_pots.append(curr_pot)

    res = []
    for res_pot in res_pots:
      curr_pot = Pot(res_pot)
      res.append(curr_pot)

    return res

    def __str__(self):
      return super().__str__()