import pygame
from enum import Enum

from objects.button import Button
from objects.gamestate import GameState

class debug():
    def __init__(self, window, colors, width, height):
        self.window = window
        self.colors = colors
        self.width = width
        self.height = height

    def load(window, colors, width, height):
        # fonts
        print('DEBUG: Making fonts')
        pygame.font.init()
        font_button = pygame.font.Font('assets/jbm-semibold.ttf', 20)
        font_header = pygame.font.Font('assets/jbm-semibold.ttf', 64)

        # buttons
        print('TITLE: Making buttons')
        button_back = Button((width/2)-100, (height/1.2), 200, 50, 'Back', colors.button_bg, colors.button_darken, font_button, colors.button_text)

        while True:
            for event in pygame.event.get():
                # mouse press
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_back.is_clicked(event.pos):
                        print('Quit button pressed')
                        return GameState.CONFIG
                # quit
                if event.type == pygame.QUIT:
                    return GameState.QUIT
        
            # fill with bg
            window.fill(colors.window_bg)

            # draw objects
            button_back.update()
            button_back.draw(window)
        
            # draw header
            #window.blit(header_surface, header_rect)

            pygame.display.update()
        