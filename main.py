import pygame
import pygame_gui # gui rewrite
import os # detect system
import ctypes # windows displays

from objects.scheme import Scheme
from objects.gamestate import GameState

from screens.play_screen import playScreen
from screens.title_screen import titleScreen
Colors = Scheme()

class xtcApp:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('xtcards')

        print('OS: '+ os.name)
        if os.name == 'nt':
            print('Detected Windows, setting ctypes.windll.user32.SetProcessDPIAware')
            #ctypes.windll.user32.SetProcessDPIAware() # fix dpi for winget_relative_rect
            dimensions = (ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1))
            print(dimensions)
            self.window = pygame.display.set_mode(dimensions, pygame.FULLSCREEN)
        else:
            display = pygame.display.Info()
            dimensions = (display.current_w, display.current_h)
            print(dimensions)   
            self.window = pygame.display.set_mode(dimensions, pygame.FULLSCREEN)
        
        self.background = pygame.Surface(dimensions)

        self.manager = pygame_gui.UIManager(window_resolution=dimensions, theme_path='data/themes/default.json')
        self.manager.add_font_paths('jb-button', 'assets/jbm-semibold.ttf')
        self.manager.add_font_paths('jb-header', 'assets/jbm-semibold.ttf')

        print('>> Initialize webcam')

    def run(self):
        game_state = GameState.TITLE # set state to Title screen
        xtTitle = titleScreen(self.manager, self.window, game_state)
        xtPlay = playScreen(self.manager, self.window, game_state)

        while True:
            if game_state == GameState.TITLE:
                print('>> SET STATE TITLE')
                xtTitle.load(self.manager, game_state)
                game_state = xtTitle.run(self.manager)
                xtTitle.delete(self.manager)

            if game_state == GameState.START:
                print('>> SET STATE START')
                xtPlay.load(self.manager, game_state)
                game_state = xtPlay.run(self.manager)
                xtPlay.delete(self.manager)

            if game_state == GameState.QUIT:
                print('>> SET STATE QUIT')
                pygame.quit()
                return
            
import os
if __name__ == "__main__":
    app = xtcApp()
    app.run()

