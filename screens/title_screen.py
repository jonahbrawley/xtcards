import pygame
import pygame_gui
from pygame_gui.elements import UIButton, UILabel, UIWindow
from objects.gamestate import GameState
from objects.scheme import Scheme

from webcam import WebcamCapture

cam = WebcamCapture(show_window=True)

class titleScreen:
    def __init__(self, manager, window):
        Colors = Scheme()

        self.width = manager.window_resolution[0]
        self.height = manager.window_resolution[1]
        self.clock = pygame.time.Clock()
        self.window = window
        self.background = pygame.Surface((self.width, self.height))
        self.background.fill(Colors.window_bg)

        self.header = None
        self.quit_button = None
        self.settings_button = None
        self.play_button = None
        self.config = None

        self.load(manager)

    def load(self, manager):
        header_rect = pygame.Rect(0, self.height*.15, self.width, 150)

        self.header = UILabel(relative_rect=header_rect,
                              text='xtcards',
                              manager=manager,
                              object_id='header',
                              anchors={
                                  'centerx': 'centerx',
                                  'top': 'top'
                              })

        quit_button_rect = pygame.Rect(0, -self.height*.13, 180, 50)
        settings_button_rect = pygame.Rect(0, -65, 180, 50)
        play_button_rect = pygame.Rect(0, -65, 180, 50)

        self.quit_button = UIButton(relative_rect=quit_button_rect,
                                                 text='Quit',
                                                 manager=manager,
                                                 anchors={
                                                     'centerx': 'centerx',
                                                     'bottom': 'bottom'
                                                 })

        self.settings_button = UIButton(relative_rect=settings_button_rect,
                                                 text='Settings',
                                                 manager=manager,
                                                 anchors={
                                                     'centerx': 'centerx',
                                                     'bottom': 'bottom',
                                                     'bottom_target': self.quit_button
                                                 })
        
        self.play_button = UIButton(relative_rect=play_button_rect,
                                                 text='Play',
                                                 manager=manager,
                                                 anchors={
                                                     'centerx': 'centerx',
                                                     'bottom': 'bottom',
                                                     'bottom_target': self.settings_button
                                                 })

    def run(self, manager):
        state = GameState.TITLE
        self.isConfClicked = False
        pos = pygame.Rect((300, 350), (350, 500))

        while True:
            time_delta = self.clock.tick(60) / 1000.0
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.quit_button:
                        print('TITLE: I should really be going!')
                        return GameState.QUIT
                    if (event.ui_element == self.settings_button and not self.isConfClicked):
                        print('TITLE: Drawing config dialog')
                        self.config = configWindow(manager=manager, pos=pos)
                        self.isConfClicked = True
                if event.type == pygame_gui.UI_WINDOW_MOVED_TO_FRONT:
                    pos = self.config.rect
                if event.type == pygame.QUIT:
                    return GameState.QUIT
                if keys[pygame.K_ESCAPE]:
                    print('TITLE: I should really be going!')
                    return GameState.QUIT

                manager.process_events(event)
            
            manager.update(time_delta)
            self.window.blit(self.background, (0,0))
            manager.draw_ui(self.window)

            pygame.display.update()

            if (self.isConfClicked):
                if not self.config.alive():
                    self.isConfClicked = False

            if (state != GameState.TITLE):
                return state
            
class configWindow(pygame_gui.elements.UIWindow):
    def __init__(self, manager, pos):
        super().__init__((pos),
                         manager,
                         window_display_title='Settings',
                         object_id='#config_window')
        
        self.debug_category_label = pygame_gui.elements.UILabel(pygame.Rect((10, 10), (150, 40)),
                                                                "Debug options",
                                                                manager=manager,
                                                                object_id="config_window_label",
                                                                container=self,
                                                                parent_element=self,
                                                                anchors={
                                                                    "left": "left"
                                                                })
        
        self.start_cam_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 10), (-1, 40)),
                                                             text='Start cam',
                                                             manager=manager,
                                                             #object_id="",
                                                             container=self,
                                                             parent_element=self,
                                                             anchors={
                                                                "top_target": self.debug_category_label,
                                                             })
        
        self.stop_cam_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 10), (-1, 40)),
                                                             text='Stop cam',
                                                             manager=manager,
                                                             #object_id="",
                                                             container=self,
                                                             parent_element=self,
                                                             anchors={
                                                                 "top_target": self.debug_category_label,
                                                                 "left_target": self.start_cam_button,
                                                                 "left": "left"
                                                             })
        
    def process_event(self, event):
        global cam
        handled = super().process_event(event)

        if (event.type == pygame_gui.UI_BUTTON_PRESSED):
            if (event.ui_element == self.start_cam_button):
                print('TITLE: Start cam')
                cam.start()
            if (event.ui_element == self.stop_cam_button):
                print('TITLE: Stop cam')
                cam.stop()
        

