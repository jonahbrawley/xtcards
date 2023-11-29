class Player:
  __ids = [] # store all player ids privately
  def __init__(self, name, chips=1000, id=None, cards=None):
    if id:
      self.id = id
    else:
      self.__generate_id()
    self.name = name
    self.chips = chips
    self.last_action = None
    self.curr_bet = 0
    self.cards = cards

  def __generate_id(self):
    if len(self.__ids) == 0:
      self.id = 0
      self.__ids.append(self.id)
    else:
      self.id = self.__ids[-1] + 1
      self.__ids.append(self.id)

  def pull_cards(self, deck):
    self.cards = [deck.pull(), deck.pull()]

  def can_do_action(self):
    return self.chips > 0 and self.last_action not in ["all_in", "fold", "out"]

  def __str__(self):
    return (
        f"Player {self.id}: {self.name}\n" +
        f"\tchips: {self.chips}\n" +
        f"\taction: {self.last_action}\n" +
        f"\tcurrent_bet: {self.curr_bet}\n" +
        f"\tcards: {self.cards}\n"
        )