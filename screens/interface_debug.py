import pygame
from objects.button import Button
from objects.gamestate import GameState
from objects.scheme import Scheme
from objects.setup_dialog import SetupDialog

class debug():
    def __init__(self, window, width, height):
        self.window = window
        self.width = width
        self.height = height

    def load(window, width, height):
        colors = Scheme()
        # fonts
        print('DEBUG: Making fonts')
        pygame.font.init()
        font_button = pygame.font.Font('assets/jbm-semibold.ttf', 20)
        font_header = pygame.font.Font('assets/jbm-semibold.ttf', 64)

        # buttons
        print('DEBUG: Making buttons')
        button_back = Button((width/2)-100, (height/1.2), 200, 50, 'Back', colors.button_bg, colors.button_darken, font_button, colors.button_text)

        # setup diag
        setupx = width/4
        setupy = 200
        setup = SetupDialog(setupx, setupy, width, height)
        moving = False

        while True:
            mousepos = pygame.mouse.get_pos()
            keys = pygame.key.get_pressed()

            button_back.update()

            if setup.is_hovered(mousepos) and button_back.is_hovered:
                button_back.is_hovered = False

            for event in pygame.event.get():
                # mouse press
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_back.is_clicked(event.pos) and setup.is_hovered(event.pos):
                        print('Ignoring button')
                    elif button_back.is_clicked(event.pos):
                        print('Back button pressed')
                        return GameState.CONFIG
                    if setup.is_hovered(event.pos):
                        moving = True
                if keys[pygame.K_ESCAPE]:
                    return GameState.CONFIG
                if (event.type == pygame.MOUSEMOTION and moving):
                    # setup.shadow_surface.fill(colors.window_bg)
                    setup.move(event.rel)
                if event.type == pygame.MOUSEBUTTONUP:
                    moving = False
                # quit
                if event.type == pygame.QUIT:
                    return GameState.QUIT
        
            # fill with bg
            window.fill(colors.window_bg)
            # window.blit(setup.shadow_surface, (0, 0))

            # draw objects
            button_back.draw(window)
            setup.draw(window)
            # pygame.transform.gaussian_blur(setup.shadow_surface, 5, repeat_edge_pixels=True)

            pygame.display.update()
        