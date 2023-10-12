import pygame
from objects.button import Button
from objects.gamestate import GameState
from objects.scheme import Scheme

# width, height in parameter is SCREEN width/height.
# it is not intended to be dialog
class SetupDialog():
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width/3, height/1.3)

    def draw(self, window):
        colors = Scheme()
        pygame.draw.rect(window, colors.button_bg, self.rect)
