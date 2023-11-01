import pygame
import pygame_gui
from pygame_gui.elements import UIButton, UILabel, UIWindow
from objects.gamestate import GameState
from objects.scheme import Scheme

from webcam import WebcamCapture

cam = WebcamCapture(show_window=True)
Colors = Scheme()
debugswitch = False # needed due to self.state class variable conundrum with configScreen

class titleScreen:
    def __init__(self, manager, window, state):
        self.state = state
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

        #self.load(manager)

    def load(self, manager, state):
        global debugswitch
        debugswitch = False
        self.state = state
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
        self.isConfClicked = False
        cfg_width = 350
        cfg_height = 500
        cfgpos = pygame.Rect((300, 350), (cfg_width, cfg_height))

        while True:
            time_delta = self.clock.tick(60) / 1000.0
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                # buttons
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.quit_button:
                        print('TITLE: I should really be going!')
                        return GameState.QUIT
                    if (event.ui_element == self.settings_button and not self.isConfClicked):
                        print('TITLE: Drawing config dialog')
                        self.config = configWindow(manager=manager, pos=cfgpos)
                        self.isConfClicked = True

                # cfg window position
                if (event.type == pygame_gui.UI_WINDOW_MOVED_TO_FRONT):
                    cfgpos = self.config.rect
                
                # cfg snap to bounds
                if (self.isConfClicked):
                    if (cfgpos.x < 0):
                        self.config.set_position((0, cfgpos.y))
                    if ((cfgpos.x+cfg_width) > manager.window_resolution[0]):
                        self.config.set_position((manager.window_resolution[0]-cfg_width, cfgpos.y))
                    if (cfgpos.y < 0):
                        self.config.set_position((cfgpos.x, 0))
                    if ((cfgpos.y+cfg_height) > manager.window_resolution[1]):
                        self.config.set_position((cfgpos.x, manager.window_resolution[1]-cfg_height))
                
                # quit program handling
                if event.type == pygame.QUIT:
                    return GameState.QUIT
                if keys[pygame.K_ESCAPE]:
                    print('TITLE: I should really be going!')
                    return GameState.QUIT

                manager.process_events(event)
            
            manager.update(time_delta)
            self.window.blit(self.background, (0,0))
            manager.draw_ui(pygame.transform.smoothscale(self.window, (3840, 2400)))

            pygame.display.flip()

            if (debugswitch):
                self.state = GameState.DEBUG

            if (self.isConfClicked):
                if not self.config.alive():
                    self.isConfClicked = False

            if (self.state != GameState.TITLE):
                return self.state
    
    def delete(self, manager):
        print('TITLE: Deleting objects')
        manager.clear_and_reset()
            
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
        
        start_width = self.start_cam_button.drawable_shape.containing_rect.width
        stop_width = self.stop_cam_button.drawable_shape.containing_rect.width
        
        self.interface_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 10), ((start_width + stop_width + 10), 40)),
                                                             text='Interface debug',
                                                             manager=manager,
                                                             container=self,
                                                             parent_element=self,
                                                             anchors={
                                                                 "top_target": self.stop_cam_button
                                                             })
        
    def process_event(self, event):
        global cam
        global debugswitch
        handled = super().process_event(event)

        if (event.type == pygame_gui.UI_BUTTON_PRESSED):
            if (event.ui_element == self.start_cam_button):
                print('TITLE: Start cam')
                cam.start()
            if (event.ui_element == self.stop_cam_button):
                print('TITLE: Stop cam')
                cam.stop()
            if (event.ui_element == self.interface_button):
                print('TITLE: Switching to debug')
                debugswitch = True
        