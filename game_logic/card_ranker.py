import itertools

class CardRanker:

  CARD_SCORE = {"2" : 12,
                "3" : 13,
                "4" : 14,
                "5" : 15,
                "6" : 16,
                "7" : 17,
                "8" : 18,
                "9" : 19,
                "T" : 20,
                "J" : 21,
                "Q" : 22,
                "K" : 23,
                "A" : 24}

  # given players, community_cards, and pots from the class constructor,
  # rank the players and determine how much money each player should win
  @staticmethod
  def rank_and_calculate_winnings(players, community_cards, pots):
    rankings = CardRanker.rank_players(players, community_cards)
    winnings = CardRanker.calculate_winnings(players, rankings, pots)
    return winnings

  # Determine the order of hand rankings
  @staticmethod
  def rank_players(players, community_cards):
    # Get a map of each player and their best hand
    hands = []
    for p in players:
      if p.last_action not in ["fold", "out"]:
        hands.append([p.id] + CardRanker.find_best_hand(p.cards, community_cards))

    # Rank the players from best to worst
    hands.sort(key=lambda x: x[1], reverse=True)

    last_score = hands[0][1]

    res = [[]]

    for hand in hands:
      if hand[1] < last_score:
        last_score = hand[1]
        res.append([hand])
      else:
        res[-1].append(hand)
    print("Rankings: (Player ID, Score, Hand Label, Hand Cards)")
    print("NOTE: Winners are in ascending order and grouped for ties (" +
          "E.g. [[p1, p2], [p3]] means p1 and p2 have the same top score and p3 is in second)\n")
    print("[")
    for group in res:
      print("  " + str(group))
    print("]")
    return res


  # Determine which hand is optimal for a given player
  @staticmethod
  def find_best_hand(p_cards, c_cards):
    best_hand = None
    best_score = None
    best_hand_label = None

    all_cards = p_cards + c_cards
    combinations = itertools.combinations(all_cards, 5)

    for combo in combinations:
      combo = CardRanker.sort_hand(list(combo))
      score, hand_label = CardRanker.evaluate_hand(combo)
      if best_score is None or score > best_score:
        best_hand = combo
        best_score = score
        best_hand_label = hand_label

    return [best_score, best_hand_label, best_hand]

  # consider the ranking order and pots to calculate each player's winnings
  @staticmethod
  def calculate_winnings(players, rankings, pots):
    # create a dictionary of { player : winnings }
    winnings = {}

    # iterate over pots in reverse with pot_index
    for pot_i in range(len(pots)):
      # -----get players to win current pot------
      rank_i = -1
      winners = []
      while len(winners) == 0:
        rank_i += 1
        for hand_ranking in rankings[rank_i]:
          p_id = hand_ranking[0] # rankings[x][0] is a player_id
          if p_id in pots[pot_i].bets.keys(): # p_id made a bet in this pot
            winners.append(p_id) # then this player is a winner of this pot

      # get the $ winnings for each person using pot.sum() / winners len
      pot_sum = pots[pot_i].sum_bets()
      pot_split_sum = int(pot_sum / len(winners))

      # add dict[p.id] += winnings for each winner
      for p_id in winners:
        winnings[p_id] = winnings.get(p_id, 0) + pot_split_sum

    # return winnings dictionary
    return winnings

  # Calculate a numerical score for a hand
  @staticmethod
  def evaluate_hand(hand):
    eval_methods = [
        CardRanker.eval_straight_flush,
        CardRanker.eval_four_of_a_kind,
        CardRanker.eval_full_house,
        CardRanker.eval_flush,
        CardRanker.eval_straight,
        CardRanker.eval_three_of_a_kind,
        CardRanker.eval_two_pair,
        CardRanker.eval_one_pair,
        CardRanker.eval_high_card
        ]

    score = None
    hand_label = None

    for method in eval_methods:
      score = method(hand)
      if score:
        score, hand_label = score
        return CardRanker.compile_score(score), hand_label

  # Convert a score into a value.
  # E.g. (2,   14, 13, 15, 12) -> 2 14 13 15 12 00 00 -> 2141315120000
  @staticmethod
  def compile_score(score):
    joint_number = ''.join(map(str, score))
    while len(joint_number) < 13:
      joint_number += "0"
    return int(joint_number)


  # sort a hand of 5 cards from lowest to highest
  @staticmethod
  def sort_hand(hand):
    for i in range(len(hand) - 1):
      min_index = i
      for j in range(i + 1, len(hand)):
        if CardRanker.score_card(hand[j]) < CardRanker.score_card(hand[min_index]):
          min_index = j
      hand[i], hand[min_index] = hand[min_index], hand[i]
    return hand

  # Card score is based on the value at [0] and not the suit at [1]
  @staticmethod
  def score_card(card):
    return CardRanker.CARD_SCORE[card[0]]

  ######################################################################
  # HAND EVALUATIONS REQUIRE 5 CARDS TO BE SORTED PRIOR TO METHOD CALL #
  ######################################################################

  # Evaluations are returned in an array with these item scores:
  # 1. hand         E.g. 0=high_card, 1=one_pair, ..., 8=straight_flush
  # 2. hand_values  E.g. 7 for pair with x77xx, OR [3, 9] for a full house with 33399
  # 3. high_cards   E.g. [8,5,4] in a deck like 22458 where (1, 2, 8, 5, 4) is returned

  # edge cases:
  # [TH JH QH KH AH] -> (8,   14)
  # [AH 2H 3H 4H 5H] -> (8,   5)
  @staticmethod
  def eval_straight_flush(hand):
    # all suits are the same
    for i in range(len(hand) - 1):
      if hand[i][1] != hand[i+1][1]:
        return None

    # Case that ace is 1
    char_values = [card[0] for card in hand]
    if char_values == ["2", "3", "4", "5", "A"]:
      return [9, 5], "Straight Flush"

    for i in range(len(hand) - 1):
      if CardRanker.score_card(hand[i]) + 1 != CardRanker.score_card(hand[i+1]):
        return None

    return [9] + [CardRanker.score_card(card) for card in reversed(hand)], "Straight Flush"

  # [JD JH JS JC AH] -> (7,   11, 14)
  @staticmethod
  def eval_four_of_a_kind(hand):
    if (hand[1][0] != hand[2][0] or hand[2][0] != hand[3][0] or
        (hand[0][0] != hand[1][0] and hand[3][0] != hand[4][0])):
        return None

    if hand[0][0] == hand[1][0]:
      return [8, CardRanker.score_card(hand[0]), CardRanker.score_card(hand[4])], "Four-of-a-Kind"
    return [8, CardRanker.score_card(hand[4]), CardRanker.score_card(hand[0])], "Four-of-a-Kind"

  # [3H 3D 3S 8C 8S] -> (6,   3, 8)
  @staticmethod
  def eval_full_house(hand):
    if (hand[0][0] != hand[1][0] or
        (hand[1][0] != hand[2][0] and hand[2][0] != hand[3][0]) or
        hand[3][0] != hand[4][0]):
      return None

    if hand[1][0] == hand[2][0]:
      return [7, CardRanker.score_card(hand[2]), CardRanker.score_card(hand[3])], "Full House"
    return [7, CardRanker.score_card(hand[2]), CardRanker.score_card(hand[1])], "Full House"



  # [2S 3S 5S 7S 9S] -> (5,   9)
  @staticmethod
  def eval_flush(hand):
    for i in range(len(hand) - 1):
      if hand[i][1] != hand[i+1][1]:
        return None

    return [6] + [CardRanker.score_card(card) for card in reversed(hand)], "Flush"

  # [3 4 5 6 7] -> (4,   7)
  @staticmethod
  def eval_straight(hand):
    # Case that ace is 1
    char_values = [card[0] for card in hand]
    if char_values == ["2", "3", "4", "5", "A"]:
      return [5, 5], "Straight"

    for i in range(len(hand) - 1):
      if CardRanker.score_card(hand[i]) + 1 != CardRanker.score_card(hand[i+1]):
        return None

    return [5, CardRanker.score_card(hand[-1])], "Straight"


  # [3 4 4 4 5] -> (3,   4, 5, 3)
  @staticmethod
  def eval_three_of_a_kind(hand):
    first = -1
    for i in range(len(hand) - 2):
      if hand[i][0] == hand[i+1][0] and hand[i][0] == hand[i+2][0]:
        first = i
        break

    if first == -1:
      return None

    res = [4]
    res.append(CardRanker.score_card(hand[first]))

    for i in reversed(range(len(hand))):
      if i == first or i == first + 1 or i == first + 2:
        continue
      res.append(CardRanker.score_card(hand[i]))

    return res, "Three-of-a-Kind"

  # [2 3 3 4 4 5] -> (2,   4, 3, 5, 2)
  @staticmethod
  def eval_two_pair(hand):
    firsts = []
    for i in range(len(hand) - 1):
      if hand[i][0] == hand[i+1][0]:
        firsts.append(i)

    if len(firsts) != 2:
      return None # 2 pairs not found

    res = [3]
    res.append(CardRanker.score_card(hand[firsts[1]]))
    res.append(CardRanker.score_card(hand[firsts[0]]))

    for i in reversed(range(len(hand))):
      if (i == firsts[0] or i == firsts[0] + 1 or
          i == firsts[1] or i == firsts[1] + 1):
        continue
      res.append(CardRanker.score_card(hand[i]))
    return res, "Two Pair"

  # [2 4 4 6 8] -> (1,   4, 8, 6, 2)
  @staticmethod
  def eval_one_pair(hand):
    first = -1
    for i in range(len(hand) - 1):
      if hand[i][0] == hand[i+1][0]:
        first = i
        break

    if first == -1:
      return None # no pair found

    res = [2]
    res.append(CardRanker.score_card(hand[first]))

    for i in reversed(range(len(hand))):
      if i == first or i == first + 1:
        continue
      res.append(CardRanker.score_card(hand[i]))

    return res, "One Pair"

  # [2, 4, 6, 8, T] -> (1,   20, 18, 16, 14, 12)
  @staticmethod
  def eval_high_card(hand):
    return [1] + [CardRanker.score_card(card) for card in reversed(hand)], "High Card"
