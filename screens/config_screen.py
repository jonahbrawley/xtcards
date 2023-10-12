import pygame
from objects.button import Button
from objects.scheme import Scheme
from objects.gamestate import GameState

def config_screen(window, width, height, cam):
    colors = Scheme()

    # fonts
    print('CONFIG: Making fonts')
    pygame.font.init()
    font_button = pygame.font.Font('assets/jbm-semibold.ttf', 20)
    font_header = pygame.font.Font('assets/jbm-semibold.ttf', 64)

    # buttons
    print('CONFIG: Making buttons')
    button_back = Button((width/2)-100, (height/1.2), 200, 50, 'Back', colors.button_bg, colors.button_darken, font_button, colors.button_text)
    button_start_webcam = Button((width/2)-400, (height/1.4), 200, 50, 'Start Webcam', colors.button_bg, colors.button_darken, font_button, colors.button_text)
    button_end_webcam = Button((width/2)-100, (height/1.4), 200, 50, 'End Webcam', colors.button_bg, colors.button_darken, font_button, colors.button_text)
    button_start_test = Button((width/2)+200, (height/1.4), 200, 50, 'Interface Test', colors.button_bg, colors.button_darken, font_button, colors.button_text)

    # create header
    print('CONFIG: Making header')
    header_surface = font_header.render('xtcards', True, colors.window_header, colors.window_bg)
    header_rect = header_surface.get_rect()
    header_rect.center = (width // 2, height // 5)

    # create texts
    print('CONFIG: Making texts')
    text_debug_surface = font_button.render('Debug options', True, colors.window_header, colors.window_bg)
    text_debug_rect = text_debug_surface.get_rect()
    text_debug_rect.center = ((width // 2)-320, height // 1.5)

    while True:
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            # mouse press
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_start_webcam.is_clicked(event.pos):
                    cam.start()
                if button_end_webcam.is_clicked(event.pos):
                    cam.stop()
                if button_back.is_clicked(event.pos):
                    return GameState.TITLE
                if button_start_test.is_clicked(event.pos):
                    print('Test run starting')
                    return GameState.DEBUG
            if keys[pygame.K_ESCAPE]:
                return GameState.TITLE
            # quit
            if event.type == pygame.QUIT:
                return GameState.QUIT
        
        # fill with black bg
        window.fill(colors.window_bg)

        # draw objects
        button_back.update()
        button_back.draw(window)
        button_start_webcam.update()
        button_start_webcam.draw(window)
        button_end_webcam.update()
        button_end_webcam.draw(window)
        button_start_test.update()
        button_start_test.draw(window)

        # draw header and texts
        window.blit(header_surface, header_rect)
        window.blit(text_debug_surface, text_debug_rect)

        pygame.display.update()