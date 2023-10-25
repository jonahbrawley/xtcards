import pygame
import pygame_gui # gui rewrite
import platform # detect system
import ctypes # windows disp

from objects.scheme import Scheme
from objects.gamestate import GameState

from webcam import WebcamCapture

from screens.interface_debug import debug
from screens.title_screen import titleScreen
from screens.config_screen import config_screen

class xtcApp:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('xtcards')

        if platform.uname().system == 'Windows':
            ctypes.windll.user32.SetProcessDPIAware() # fix dpi for win
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
        self.cam = WebcamCapture(show_window=True)

    def run(self):
        game_state = GameState.TITLE # set state to Title screen

        while True:
            if game_state == GameState.TITLE:
                print('>> SET STATE TITLE')
                xtTitle = titleScreen(self.manager, self.window)
                game_state = xtTitle.run(self.manager)
            #if game_state == GameState.START:
                #game_state = play_game(window)
            if game_state == GameState.CONFIG:
                print('>> SET STATE CONFIG')
                #game_state = config_screen(window, width, height, cam)
            if game_state == GameState.DEBUG:
                print('>> SET STATE DEBUG')
                #game_state = debug.load(window, width, height)
            if game_state == GameState.QUIT:
                print('>> SET STATE QUIT')
                pygame.quit()
                return
            
if __name__ == "__main__":
    app = xtcApp()
    app.run()