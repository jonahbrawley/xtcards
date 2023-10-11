import pygame
from enum import Enum
from objects.button import Button

class interface_debug:
    def __init__(self, window, state):
        self.state = state
        self.window = window
    
    def load():
        # fonts
        print('DEBUG: Making fonts')
        pygame.font.init()
        font_button = pygame.font.Font('assets/jbm-semibold.ttf', 20)
        font_header = pygame.font.Font('assets/jbm-semibold.ttf', 64)

        # buttons
        print('TITLE: Making buttons')
        button_back = Button((width/2)-100, (height/1.2), 200, 50, 'Back', color_button_bg, color_button_darken, font_button, color_button_text)

        return state