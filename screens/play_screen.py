import pygame
import pygame_gui
from objects.gamestate import GameState
from objects.scheme import Scheme
from objects.setup import setupWindow

homeswitch = False

class playScreen:
    def __init__(self, manager, window, state):
        Colors = Scheme()
        self.state = state

        self.width = manager.window_resolution[0]
        self.height = manager.window_resolution[1]
        self.clock = pygame.time.Clock()
        self.window = window
        self.background = pygame.Surface((self.width, self.height))
        self.background.fill(Colors.window_bg)
        #self.darken = pygame.Surface((self.width, self.height))
        #self.darken.fill((0, 0, 0, 40)) # fill with black color alpha 40
        self.darken_rect = pygame.Rect((0,0), (self.width, self.height))

        self.header = None

    def load(self, manager, state):
        self.state = state
        
        stp_width = 500
        stp_height = 500
        stppos = pygame.Rect(((self.width/2)-(stp_width/2), (self.height/2)-(stp_height/2)), (stp_width, stp_height))

        #pause button
        pause_button_rect = pygame.Rect(15, 15, 100, 50)
        self.pause_button = pygame_gui.elements.UIButton(relative_rect=pause_button_rect,
                                            text='Pause',
                                            manager=manager,
                                            anchors={
                                            'left': 'left',
                                            'top': 'top'
                                            })
        self.pause_button.hide()

        self.setup = setupWindow(manager, stppos)

    def run(self, manager):
        global homeswitch
        darken = False
        pauseClicked = False

        # pause set up
        pause_width = 350
        pause_height = 400
        pausepos = pygame.Rect(((self.width/2)-(pause_width/2), (self.height/2)-(pause_height/2)), (pause_width, pause_height))
        
        # player set up
        players_width = self.width*.3
        players_height = self.height*.6
        playerspos = pygame.Rect((10, self.height-(players_height+10)), (players_width, players_height))

        while True:
            time_delta = self.clock.tick(60) / 1000.0
            keys = pygame.key.get_pressed()

            # if setup window is closed, open player window and pause button
            if(setupWindow.startClicked):
                #player widnow
                self.players = playerWindow(manager=manager, pos=playerspos)
                # show pause button
                self.pause_button.show()
                setupWindow.startClicked = False

            for event in pygame.event.get():
                #if pause button is clicked
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if (event.ui_element == self.pause_button and not pauseClicked):
                            print('TITLE: Drawing pause dialog')
                            pauseClicked = True
                            darken = True
                            self.pause = pauseWindow(manager=manager, pos=pausepos)
                            self.pause.set_blocking(True)
                if event.type == pygame.QUIT:
                    return GameState.QUIT
                if keys[pygame.K_ESCAPE]:
                    print('DEBUG: Switching to TITLE')
                    self.state = GameState.TITLE

                manager.process_events(event)

            manager.update(time_delta)
            self.window.blit(self.background, (0,0))

            manager.draw_ui(self.window)

            
            if (pauseClicked):
                if not self.pause.alive():
                    darken = False
                    pauseClicked = False

            if (darken):
                # self.window.blit(self.darken, (0,0)) # add dark overlay
                # pygame.draw.rect(self.window, (0,0,0,40), self.darken_rect)
                # self.pause.change_layer(3)
                temp = 1

            pygame.display.update()

            if (homeswitch):
                self.state = GameState.TITLE
                homeswitch = False

            if (self.state != GameState.START):
                return self.state
    
    def delete(self, manager):
        print('DEBUG: Deleting objects')
        manager.clear_and_reset()

class pauseWindow(pygame_gui.elements.UIWindow):
    def __init__(self, manager, pos):
        super().__init__((pos),
                        manager,
                        window_display_title='Pause',
                        object_id='#pause_window',
                        draggable=False)
        self.resume_button = pygame_gui.elements.UIButton(pygame.Rect((0, 400/4), (150, 40)),
                                                                "Resume",
                                                                manager=manager,
                                                                object_id="pause_window_label",
                                                                container=self,
                                                                parent_element=self,
                                                                anchors={
                                                                    "centerx": "centerx"
                                                                })
                
        self.save_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 10), ((200), 40)),
                                                            text='Save and Quit',
                                                            manager=manager,
                                                            container=self,
                                                            parent_element=self,
                                                            anchors={
                                                                "top_target": self.resume_button,
                                                                "centerx": "centerx"
                                                            })
        
        self.quit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 10), ((200), 40)),
                                                            text='Abandon Game',
                                                            manager=manager,
                                                            container=self,
                                                            parent_element=self,
                                                            anchors={
                                                                "top_target": self.save_button,
                                                                "centerx": "centerx"
                                                            })
        
    def process_event(self, event):
        global homeswitch
        handled = super().process_event(event)

        if (event.type == pygame_gui.UI_BUTTON_PRESSED):
            if (event.ui_element == self.quit_button):
                homeswitch = True
            if (event.ui_element == self.resume_button):
                self.kill()
            if (event.ui_element == self.save_button):
                homeswitch = True

class playerWindow(pygame_gui.elements.UIWindow):
    def __init__(self, manager, pos):
        super().__init__((pos),
                        manager,
                        window_display_title='Players',
                        object_id='#setup_window',
                        draggable=False)
        self.numplayer_label = pygame_gui.elements.UILabel(pygame.Rect((20, 20), (180, 40)),
                                                                    "players 1",
                                                                    manager=manager,
                                                                    object_id="config_window_label",
                                                                    container=self,
                                                                    parent_element=self,
                                                                    anchors={
                                                                        "left": "left"
                                                                    })
        # for i in setupWindow.player_count:
        #     self.numplayer_label = pygame_gui.elements.UILabel(pygame.Rect((20, 20), (180, 40)),
        #                                                             "players "+str(i)+": ",
        #                                                             manager=manager,
        #                                                             object_id="config_window_label",
        #                                                             container=self,
        #                                                             parent_element=self,
        #                                                             anchors={
        #                                                                 "left": "left"
        #                                                             })
