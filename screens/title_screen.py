import pygame
import pygame_gui
from pygame_gui.elements import UIButton
from objects.gamestate import GameState
from objects.scheme import Scheme

class titleScreen:
    def __init__(self, manager, window):
        self.is_running = False

        Colors = Scheme()

        self.width = manager.window_resolution[0]
        self.height = manager.window_resolution[1]
        self.clock = pygame.time.Clock()
        self.window = window
        self.background = pygame.Surface((self.width, self.height))
        self.background.fill(Colors.window_bg)
        
        self.load(manager)
        self.run(manager)

    def load(self, manager):
        self.test_button = UIButton(pygame.Rect((int(self.width/2),
                                                 int(self.height*.9)),
                                                 (110, 40)),
                                                 'EVERYTHING',
                                                 manager)

        # self.test_button_2 = UIButton(pygame.Rect((int(self.options.resolution[0] / 3),
        #                                            int(self.options.resolution[1] * 0.90)),
        #                                           (110, 40)),
        #                               'EVERYTHING',
        #                               self.ui_manager,
        #                               object_id='#everything_button')
        self.is_running = True
    
    def run(self, manager):
        while (self.is_running):
            time_delta = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                    return GameState.QUIT
            
            manager.update(time_delta)
            self.window.blit(self.background, (0,0))
            manager.draw_ui(self.window)

            pygame.display.update()

"""
def title_screen(window, width, height):
    colors = Scheme()

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
"""