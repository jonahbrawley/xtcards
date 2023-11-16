import pygame
import pygame_gui
from pygame_gui.elements import UILabel
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
        
        header_rect = pygame.Rect(0, self.height*.01, self.width//3, 150)

        self.header = UILabel(relative_rect=header_rect,
                            text='Set Up Names...',
                            manager=manager,
                            object_id='header_game',
                            anchors={
                                'centerx': 'centerx',
                                'top': 'top'
                            })
        self.header.hide()

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
        players_width = self.width*.25
        players_height = self.height*.5
        playerspos = pygame.Rect((10, self.height-(players_height+10)), (players_width, players_height))

        # bank set up
        bank_width = self.width*.25
        bank_height = self.height*.5
        bankpos = pygame.Rect((self.width - (bank_width+10), self.height-(bank_height+10)), (bank_width, bank_height))

        # player name set up
        playerSetup_width = self.width*.26
        playerSetup_height = self.height*.46
        playerSetuppos = pygame.Rect(((self.width/2)-(playerSetup_width/2), (self.height/2)-(playerSetup_height/2)), (playerSetup_width, playerSetup_height))


        while True:
            time_delta = self.clock.tick(60) / 1000.0
            keys = pygame.key.get_pressed()

            # if setup window is closed, open player window and pause button
            if(setupWindow.startClicked):
                self.playerSetUp = playerNameSetUp(manager=manager, pos=playerSetuppos)
                setupWindow.startClicked = False

            if(playerNameSetUp.submitPlayerClicked):
                #player widnow
                self.players = playerWindow(manager=manager, pos=playerspos)
                # show pause button
                self.pause_button.show()
                # show header
                self.header.show()
                #build bank
                self.bank = bankWindow(manager=manager, pos=bankpos)
                playerNameSetUp.submitPlayerClicked = False

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
        self.resume_button = pygame_gui.elements.UIButton(pygame.Rect((0, 400/4), (300, 40)),
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

        v_pad = 30

        super().__init__((pos),
                        manager,
                        window_display_title='Players',
                        object_id='#setup_window',
                        draggable=False)
        self.numplayer_label = pygame_gui.elements.UILabel(pygame.Rect((20, 20), (300, 40)),
                                                                    "players | chips | action",
                                                                    manager=manager,
                                                                    object_id="config_window_label",
                                                                    container=self,
                                                                    parent_element=self,
                                                                    anchors={
                                                                        "centerx": "centerx"
                                                                    })
        self.player_labels_list = []
        for i in range(len(playerNameSetUp.playerNames)):
            self.players_label = pygame_gui.elements.UILabel(pygame.Rect((20, v_pad), (180, 40)),
                                                                    playerNameSetUp.playerNames.index(i)+ "shbf",
                                                                    manager=manager,
                                                                    object_id="config_window_label",
                                                                    container=self,
                                                                    parent_element=self,
                                                                    anchors={
                                                                        "left": "left"
                                                                    })
            self.player_labels_list.append(self.players_label)
            v_pad += 50

class bankWindow(pygame_gui.elements.UIWindow):
    def __init__(self, manager, pos):
        super().__init__((pos),
                        manager,
                        window_display_title='The Holy Bank',
                        object_id='#setup_window',
                        draggable=False)
        self.bank_label = pygame_gui.elements.UILabel(pygame.Rect((0, 20), (180, 40)),
                                                                    "Value:",
                                                                    manager=manager,
                                                                    object_id="header_game",
                                                                    container=self,
                                                                    parent_element=self,
                                                                    anchors={
                                                                        "top": "top",
                                                                        "centerx": "centerx"
                                                                    })
        self.value_label = pygame_gui.elements.UILabel(pygame.Rect((0, 20), (180, 40)),
                                                                    "0",
                                                                    manager=manager,
                                                                    object_id="header_game",
                                                                    container=self,
                                                                    parent_element=self,
                                                                    anchors={
                                                                        "top_target": self.bank_label,
                                                                        "centerx": "centerx"
                                                                    })
        self.log_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, -60), ((100), 40)),
                                                            text='Log',
                                                            manager=manager,
                                                            container=self,
                                                            parent_element=self,
                                                            anchors={
                                                                "bottom": "bottom",
                                                                "centerx": "centerx"
                                                            })
        
class playerNameSetUp(pygame_gui.elements.UIWindow):
    submitPlayerClicked = False
    ai_player_count = 1
    playerNames = []

    def __init__(self, manager, pos):
        super().__init__((pos),
                        manager,
                        window_display_title='Player Names',
                        object_id='#setup_window',
                        draggable=False)
        v_pad = 30
        h_pad = 30

        self.player_name = []
        self.player_name_labels = []
        for i in range(setupWindow.player_count):
            player_name_label = pygame_gui.elements.UITextEntryLine(
            pygame.Rect((h_pad, v_pad), (180, 40)),
            initial_text=f"player{i+1}",  # Use f-string to include the player number in the initial text
            placeholder_text="Player Name",
            container=self,
            parent_element=self,
            anchors={"left": "left"}
            )
            self.player_name_labels.append(player_name_label)  # Add the label to the list
            v_pad += 50
        self.submit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, -60), ((160), 40)),
                                                            text='Submit',
                                                            manager=manager,
                                                            container=self,
                                                            parent_element=self,
                                                            anchors={
                                                                "bottom": "bottom",
                                                                "centerx": "centerx"
                                                            })
            
    def process_event(self, event):
        global playerNames

        handled = super().process_event(event)

        if (event.type == pygame_gui.UI_BUTTON_PRESSED):
            if (event.ui_element == self.submit_button):
                self.player_name = [label.get_text() for label in self.player_name_labels]
                playerNames = self.player_name
                playerNameSetUp.submitPlayerClicked = True
                self.kill()
                print(self.player_name)
