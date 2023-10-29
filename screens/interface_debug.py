import pygame
import pygame_gui
from pygame_gui.elements import UIButton, UILabel, UIWindow
from objects.gamestate import GameState
from objects.scheme import Scheme

class debugScreen:
    def __init__(self, manager, window, state):
        Colors = Scheme()
        self.state = state

        self.width = manager.window_resolution[0]
        self.height = manager.window_resolution[1]
        self.clock = pygame.time.Clock()
        self.window = window
        self.background = pygame.Surface((self.width, self.height))
        self.background.fill(Colors.window_bg)

        self.header = None

        #self.load(manager)

    def load(self, manager, state):
        self.state = state
        header_rect = pygame.Rect(0, self.height*.15, self.width, 150)
        
        self.header = UILabel(relative_rect=header_rect,
                              text='debug',
                              manager=manager,
                              object_id='header',
                              anchors={
                                  'centerx': 'centerx',
                                  'top': 'top'
                              })

    def run(self, manager):
        while True:
            time_delta = self.clock.tick(60) / 1000.0
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return GameState.QUIT
                if keys[pygame.K_ESCAPE]:
                    print('DEBUG: Switching to TITLE')
                    self.state = GameState.TITLE

                manager.process_events(event)

            manager.update(time_delta)
            self.window.blit(self.background, (0,0))
            manager.draw_ui(self.window)

            pygame.display.update()

            if (self.state != GameState.DEBUG):
                return self.state
    
    def delete(self, manager):
        print('DEBUG: Deleting objects')
        manager.clear_and_reset()