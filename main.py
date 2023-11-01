import pygame
import pygame_gui # gui rewrite
import os # detect system
import ctypes # windows disp

from objects.scheme import Scheme
from objects.gamestate import GameState

from screens.interface_debug import debugScreen
from screens.title_screen import titleScreen
#from screens.config_screen import config_screen

Colors = Scheme()

class xtcApp:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('xtcards')

        print('OS: '+ os.name)
        if os.name == 'nt':
            print('Detected Windows, setting ctypes.windll.user32.SetProcessDPIAware')
            ctypes.windll.user32.SetProcessDPIAware() # fix dpi for winget_relative_rect
        display = pygame.display.Info()
        dimensions = (display.current_w, display.current_h)
        
        self.window = pygame.display.set_mode(dimensions, pygame.FULLSCREEN)
        self.background = pygame.Surface(dimensions)

        self.manager = pygame_gui.UIManager(dimensions, 'data/themes/default.json')
        self.manager.set_window_resolution(dimensions)
        self.manager.add_font_paths('jb-button', 'assets/jbm-semibold.ttf')
        self.manager.add_font_paths('jb-header', 'assets/jbm-semibold.ttf')
        fonts = [
            {'name': 'jb-button', 'point_size': 20, 'style': 'regular'},
            {'name': 'jb-header', 'point_size': 64, 'style': 'regular'},
        ]
        self.manager.preload_fonts(fonts)

        print('>> Initialize webcam')

    def run(self):
        game_state = GameState.TITLE # set state to Title screen
        xtTitle = titleScreen(self.manager, self.window, game_state)
        xtDebug = debugScreen(self.manager, self.window, game_state)

        while True:
            if game_state == GameState.TITLE:
                print('>> SET STATE TITLE')
                xtTitle.load(self.manager, game_state)
                game_state = xtTitle.run(self.manager)
                xtTitle.delete(self.manager)

            #if game_state == GameState.START:
                #game_state = play_game(window)

            if game_state == GameState.DEBUG:
                print('>> SET STATE DEBUG')
                xtDebug.load(self.manager, game_state)
                game_state = xtDebug.run(self.manager)
                xtDebug.delete(self.manager)

            if game_state == GameState.QUIT:
                print('>> SET STATE QUIT')
                pygame.quit()
                return
            
if __name__ == "__main__":
    app = xtcApp()
    app.run()