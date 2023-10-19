import pygame
from objects.dialog import Dialog
from objects.scheme import Scheme

# width, height is SCREEN width/height.
class SetupDialog(Dialog): # extends Dialog
    def __init__(self, x, y, width, height):
        colors = Scheme()
        self.boxwidth = width/3
        self.boxheight = height/3
        self.rect = pygame.Rect(x, y, self.boxwidth, self.boxheight)

    def draw(self, window):
        colors = Scheme()
        pygame.draw.rect(window, colors.button_bg, self.rect)
        
    def is_hovered(self, pos):
        if self.rect.collidepoint(*pos):
            return True
        return False
    
    def move(self, rel):
        self.rect.move_ip(rel)
