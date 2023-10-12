import pygame
import platform # detect system
import ctypes # windows disp

from objects.button import Button
from objects.scheme import Scheme
from objects.gamestate import GameState

from screens.interface_debug import debug

from webcam import WebcamCapture

if platform.uname().system == 'Windows':
    ctypes.windll.user32.SetProcessDPIAware() # fix dpi for win

from screens.title_screen import title_screen
from screens.config_screen import config_screen

pygame.init()
dimensions = pygame.display.Info() # get screen dimensions
window = pygame.display.set_mode((dimensions.current_w, dimensions.current_h), pygame.FULLSCREEN)
pygame.display.set_caption('xtcards')

game_state = GameState.TITLE # set state to Title screen
colors = Scheme() # colorscheme

width = window.get_width()
height = window.get_height()

# Webcam
print('>> SETUP: Initialize webcam')
cam = WebcamCapture(show_window=True)

def main():
    global game_state
    # main window loop
    while True:
        if game_state == GameState.TITLE:
            print('>> SETUP: SET STATE TITLE')
            game_state = title_screen(window, colors, width, height, game_state)
        #if game_state == GameState.START:
            #game_state = play_game(window)
        if game_state == GameState.CONFIG:
            print('>> SETUP: SET STATE CONFIG')
            game_state = config_screen(window, colors, width, height, cam, game_state)
        if game_state == GameState.DEBUG:
            print('>> SETUP: SET STATE DEBUG')
            game_state = debug.load(window, colors, width, height)
        if game_state == GameState.QUIT:
            print('>> SETUP: SET STATE QUIT')
            pygame.quit()
            return

if __name__ == "__main__":
    main()