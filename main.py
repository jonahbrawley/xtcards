import pygame
from button import Button
from webcam import WebcamCapture
from enum import Enum

class GameState(Enum):
    QUIT = -1
    TITLE = 0
    START = 1
    CONFIG = 2

pygame.init()
dimensions = pygame.display.Info() # get screen dimensions
window = pygame.display.set_mode((dimensions.current_w, dimensions.current_h), pygame.FULLSCREEN)
pygame.display.set_caption('xtcards')

game_state = GameState.TITLE # set state to Title screen

# colors
color_window_bg = (108, 96, 97) # Wenge - 6C6061
color_window_darken = (100, 64, 62) # Rose ebony - 64403E
color_button_text = (226, 229, 220) # Alablaster - E2E5DC
color_button_bg = (162, 174, 152) # Ash gray - A2AE98
color_button_darken = (131, 142, 131) # Battleship gray - 838E83

width = window.get_width()
height = window.get_height()

# Webcam
print('SETUP: Initialize webcam')
cam = WebcamCapture(show_window=True)

def main():
    global game_state
    # main window loop
    while True:
        if game_state == GameState.TITLE:
            print('STATE: SET TITLE')
            game_state = title_screen(window)
        #if game_state == GameState.START:
            #game_state = play_game(window)
        #if game_state == GameState.CONFIG:
            #game_state = config_screen(window)
        if game_state == GameState.QUIT:
            print('Quitting...')
            pygame.quit()
            return

def title_screen(window):
    global game_state
    # fonts
    print('TITLE: Making fonts')
    pygame.font.init()
    font_button = pygame.font.Font('assets/jbm-semibold.ttf', 20)
    font_header = pygame.font.Font('assets/jbm-semibold.ttf', 64)

    # buttons
    print('TITLE: Making buttons')
    button_quit = Button((width/2)-100, (height/1.2), 200, 50, 'Quit', color_button_bg, color_button_darken, font_button, color_button_text)
    button_start_webcam = Button((width/2)+150, (height/1.2), 200, 50, 'Start Webcam', color_button_bg, color_button_darken, font_button, color_button_text)
    button_end_webcam = Button((width/2)+400, (height/1.2), 200, 50, 'End Webcam', color_button_bg, color_button_darken, font_button, color_button_text)

    # create header
    print('TITLE: Making header')
    header_surface = font_header.render('xtcards', True, color_button_text, color_window_bg)
    header_rect = header_surface.get_rect()
    header_rect.center = (width // 2, height // 5)

    while True:
        for event in pygame.event.get():
            # mouse press
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_quit.is_clicked(event.pos):
                    print('Quit button pressed')
                    return GameState.QUIT
                if button_start_webcam.is_clicked(event.pos):
                    cam.start()
                if button_end_webcam.is_clicked(event.pos):
                    cam.stop()
            # quit
            if event.type == pygame.QUIT:
                return GameState.QUIT
        
        # fill with black bg
        window.fill(color_window_bg)

        # draw objects
        button_quit.update()
        button_quit.draw(window)
        button_start_webcam.update()
        button_start_webcam.draw(window)
        button_end_webcam.update()
        button_end_webcam.draw(window)

        # draw header
        window.blit(header_surface, header_rect)

        pygame.display.update()

if __name__ == "__main__":
    main()