import pygame
from objects.button import Button
from enum import Enum
from objects.scheme import Scheme
from objects.gamestate import GameState


def title_screen(window, colors, width, height, game_state):

    # fonts
    print('TITLE: Making fonts')
    pygame.font.init()
    font_button = pygame.font.Font('assets/jbm-semibold.ttf', 20)
    font_header = pygame.font.Font('assets/jbm-semibold.ttf', 64)

    # buttons
    print('TITLE: Making buttons')
    button_start = Button((width/2)-100, (height)/1.42, 200, 50, 'Start', colors.button_bg, colors.button_darken, font_button, colors.button_text)
    button_settings = Button((width/2)-100, (height)/1.3, 200, 50, 'Config', colors.button_bg, colors.button_darken, font_button, colors.button_text)
    button_quit = Button((width/2)-100, (height/1.2), 200, 50, 'Quit', colors.button_bg, colors.button_darken, font_button, colors.button_text)

    # create header
    print('TITLE: Making header')
    header_surface = font_header.render('xtcards', True, colors.window_header, colors.window_bg)
    header_rect = header_surface.get_rect()
    header_rect.center = (width // 2, height // 5)

    while True:
        for event in pygame.event.get():
            # mouse press
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_quit.is_clicked(event.pos):
                    print('Quit button pressed')
                    return GameState.QUIT
                if button_settings.is_clicked(event.pos):
                    print('Config button pressed')
                    return GameState.CONFIG
            # quit
            if event.type == pygame.QUIT:
                return GameState.QUIT
        
        # fill with black bg
        window.fill(colors.window_bg)

        # draw objects
        button_start.update()
        button_start.draw(window)
        button_settings.update()
        button_settings.draw(window)
        button_quit.update()
        button_quit.draw(window)
        
        # draw header
        window.blit(header_surface, header_rect)

        pygame.display.update()