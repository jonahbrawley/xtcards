import sys
sys.path.append('../')
from webcam import WebcamCapture

import random


class Deck:
  UNKNOWN_CARD_SYMBOL = 'NA'
  FULL_DECK = ['AH', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', 'TH', 'JH', 'QH', 'KH', 'AD', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', 'TD', 'JD', 'QD', 'KD', 'AC', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', 'TC', 'JC', 'QC', 'KC', 'AS', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', 'TS', 'JS', 'QS', 'KS']

  def __init__(self):
    self.cards = Deck.FULL_DECK[:]
    random.shuffle(self.cards)
    self.scanning_active = False

  def pull(self):
    if len(self.cards) == 0:
      print("Error: Cannot pull a card, deck is empty.")
      return None

    res = self.cards.pop()
    return res

  def set_scanning_status(self, status=True):
    if self.scanning_active == status:
      print(f"status already set to: {status}")
      return

    self.scanning_active = status

    if status:
      self.webcam = WebcamCapture(show_window=True)
      self.webcam.start()
    else:
      self.webcam.stop()
      self.webcam = None
  
  def scan(self):
    if self.webcam is not None and self.webcam.is_frame_not_null():
      res = self.webcam.detect_card()
      return res
    else:
      return None