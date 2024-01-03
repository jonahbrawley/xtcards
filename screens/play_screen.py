from random import shuffle
import pygame
import pygame_gui

from pygame_gui.elements import UILabel
from objects.screenstate import ScreenState
from objects.scheme import Scheme
from objects.setup import setupWindow
#from game_logic.game import GameState

import pygame.camera

homeswitch = False
drawcam = False

class playScreen:
    playerNames = []
    def __init__(self, manager, window, state):
        Colors = Scheme()
        self.state = state
        
        self.width = manager.window_resolution[0]
        self.height = manager.window_resolution[1]
        self.clock = pygame.time.Clock()
        self.window = window
        self.background = pygame.Surface((self.width, self.height))
        self.background.fill(Colors.window_bg)
        self.darken_rect = pygame.Rect((0,0), (self.width, self.height))

        self.header = None
        self.camwindow = None
        self.betwindow = None

        self.camClicked = False # TEMP
        self.betClicked = False # TEMP

        # Class variable for a new GameState from game_logic/game.py.
        # This variable is updated after number of players/AI is selected.

        # For future save game functions, this class variable should be loaded
        # from the saved game's GameState object.
        # (more on this functionality later)
        self.game_state = None

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

        self.showcam_button = pygame_gui.elements.UIButton(relative_rect=pause_button_rect,
                                            text='camwin',
                                            manager=manager,
                                            anchors={
                                            'left': 'left',
                                            'top': 'top',
                                            'left_target': self.pause_button
                                            })
        self.showcam_button.hide()

        self.showbet_button = pygame_gui.elements.UIButton(relative_rect=pause_button_rect,
                                            text='betwin',
                                            manager=manager,
                                            anchors={
                                            'left': 'left',
                                            'top': 'top',
                                            'left_target': self.showcam_button
                                            })
        self.showbet_button.hide()

        #info button
        info_button_rect = pygame.Rect(-55, 15, 40, 50)
        self.info_button = pygame_gui.elements.UIButton(relative_rect=info_button_rect,
                                                text='i',
                                                manager=manager,
                                                anchors={
                                                'right': 'right'
                                                })
        self.info_button.hide()

        #donation button
        church_button_rect = pygame.Rect(-110, 15, 40, 50)
        self.church_button = pygame_gui.elements.UIButton(relative_rect=church_button_rect,
                                                          text='$',
                                                          manager=manager,
                                                          anchors={
                                                          'right': 'right'
                                                          })
        self.church_button.hide()

        self.setup = setupWindow(manager, stppos)

    def run(self, manager):
        global homeswitch
        pauseClicked = False
        infoClicked = False
        churchClicked = False

        # pause set up
        pause_width = 350
        pause_height = 400
        pausepos = pygame.Rect(((self.width/2)-(pause_width/2), (self.height/2)-(pause_height/2)), (pause_width, pause_height))
        
        # player set up
        players_width = self.width*.25
        players_height = self.height*.55
        playerspos = pygame.Rect((10, self.height-(players_height+10)), (players_width, players_height))

        # bank set up
        bank_width = self.width*.25
        bank_height = self.height*.55
        bankpos = pygame.Rect((self.width - (bank_width+10), self.height-(bank_height+10)), (bank_width, bank_height))

        # player name set up
        playerSetup_width = self.width*.26
        playerSetup_height = self.height*.46
        playerSetuppos = pygame.Rect(((self.width/2)-(playerSetup_width/2), (self.height/2)-(playerSetup_height/2)), (playerSetup_width, playerSetup_height))

        # bet set up TEMP
        bet_width = self.width*.25
        bet_height = self.height*.50
        betpos = pygame.Rect(((self.width*.50)-(bet_width//2), self.height*.25), (bet_width, bet_height))

        # cam set up TEMP
        cam_width = self.width*.50
        cam_height = self.height*.75
        campos = pygame.Rect(((self.width*.5)-(cam_width//2), self.height*.125), (cam_width, cam_height))

        pygame.camera.init()
        info_width = 175
        info_height = 400
        infopos = pygame.Rect(((self.width/2)-(info_width/2), (self.height/2)-(info_height/2)), (info_width, info_height))

        #info icon set up
        info_width = self.width*.20
        info_height = self.height*.4
        infopos = pygame.Rect(((self.width)-(info_width+10), (self.height/2)-(info_height)), (info_width, info_height))

        #church icon set up
        church_width = self.width*.20
        church_height = self.height*.4
        churchpos = pygame.Rect(((self.width)-(church_width*3), (self.height/2)-(church_height/2)), (church_width, church_height))

        while True:
            global drawcam
            time_delta = self.clock.tick(60) / 1000.0
            keys = pygame.key.get_pressed()

            # if setup window is closed, open player window and pause button
            if(setupWindow.startClicked):
                # show header
                self.header.show()
                self.playerSetUp = playerNameSetUp(manager=manager, pos=playerSetuppos) # loads player name setup
                setupWindow.startClicked = False

            if(playerNameSetUp.submitPlayerClicked):
                print("BEFORE: -----------" + str(len(playScreen.playerNames)) + "-----------")
                #player window
                self.players = playerWindow(manager=manager, pos=playerspos)
                # show pause button
                self.pause_button.show()

                self.showcam_button.show()
                self.showbet_button.show()
                # hide header
                self.header.hide()
                #build bank
                self.bank = bankWindow(manager=manager, pos=bankpos)
                playerNameSetUp.submitPlayerClicked = False
                self.header.show()
                #show info button
                self.info_button.show()
                #show donation button
                self.church_button.show()
                self.bank = bankWindow(manager=manager, pos=bankpos)

                setupWindow.startClicked = False # why is this here?

            for event in pygame.event.get():
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    # PAUSE BUTTON
                    if (event.ui_element == self.pause_button and not pauseClicked):
                            print('TITLE: Drawing pause dialog')
                            pauseClicked = True
                            darken = True
                            self.pause = pauseWindow(manager=manager, pos=pausepos)
                            self.pause.set_blocking(True)
                    
                    # TEMP CAMERA TESTS
                    if (event.ui_element == self.showcam_button):
                        if (not self.camClicked):
                            print('OPENING CAM')
                            self.camwindow = camWindow(manager, campos)
                            self.camClicked = True
                        elif (self.camClicked):
                            print('KILLING CAM')
                            drawcam = False
                            self.camClicked = False
                            self.camwindow.webcam.stop()
                            self.camwindow.kill()
                            self.camwindow = None
                    
                    # TEMP BET TESTS
                    if (event.ui_element == self.showbet_button):
                        if (not self.betClicked):
                            print('OPENING BET')
                            self.betwindow = betWindow(manager, betpos)
                            self.betClicked = True
                        elif (self.betClicked):
                            print('KILLING BET')
                            self.betwindow.kill()
                            self.betwindow = None
                            self.betClicked = False

                    # INFO BUTTON
                    if (event.ui_element == self.info_button and not infoClicked):
                            print('TITLE: Drawing info dialog')
                            infoClicked = True
                            darken = True
                            self.info = infoWindow(manager=manager, pos=infopos)
                            self.info.set_blocking(False)
                            self.info.load_text("assets/poker_rules.txt")

                    # DONATION BUTTON
                    if (event.ui_element == self.church_button and not churchClicked):
                        print('TITLE: Drawing donation dialog')
                        churchClicked = True
                        darken = True
                        self.church = churchWindow(manager=manager, pos=churchpos)
                        self.church.set_blocking(False)

                if event.type == pygame.QUIT:
                    return ScreenState.QUIT
                if keys[pygame.K_ESCAPE]:
                    print('DEBUG: Switching to TITLE')
                    self.state = ScreenState.TITLE

                manager.process_events(event)

            manager.update(time_delta)
            self.window.blit(self.background, (0,0))
            if self.camwindow != None:
                print('drawing')
                drawcam = True
                self.camwindow.draw_camera()

            

            manager.draw_ui(self.window)

            # Check and reset flags
            if (pauseClicked):
                if not self.pause.alive():
                    pauseClicked = False
            if (infoClicked):
                if not self.info.alive():
                    infoClicked = False
            if (churchClicked):
                if not self.church.alive():
                    churchClicked = False

            pygame.display.update()

            if (homeswitch):
                self.state = ScreenState.TITLE
                homeswitch = False
            if (self.state != ScreenState.START):
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
        self.resume_button = pygame_gui.elements.UIButton(pygame.Rect((0, 400/4), (200, 40)),
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
    aiPlayerNames = ["HolyBot", "AngelAI", "GodBot", "NoahsAI"]
    shuffle(aiPlayerNames)
    def __init__(self, manager, pos):

        v_pad = 10

        super().__init__((pos),
                        manager,
                        window_display_title='Players',
                        object_id='#setup_window',
                        draggable=False)
        self.numplayer_label = pygame_gui.elements.UILabel(pygame.Rect((20, 20), (300, 40)),
                                                                    "players : chips | action",
                                                                    manager=manager,
                                                                    object_id="config_window_label",
                                                                    container=self,
                                                                    parent_element=self,
                                                                    anchors={
                                                                        "centerx": "centerx"
                                                                    })
        self.player_labels_list = []
        for i in range(len(playScreen.playerNames)):
            self.players_label = pygame_gui.elements.UILabel(pygame.Rect((20, v_pad), (180, 40)),
                                                                    playScreen.playerNames[i]+ ":  " + str(setupWindow.chip_count) + "  |  ",
                                                                    manager=manager,
                                                                    object_id="config_window_label",
                                                                    container=self,
                                                                    parent_element=self,
                                                                    anchors={
                                                                        "left": "left",
                                                                        "top_target": self.numplayer_label
                                                                    })
            self.player_labels_list.append(self.players_label)
            v_pad += 50
        for i in range(setupWindow.ai_player_count):
            self.ai_players_label = pygame_gui.elements.UILabel(pygame.Rect((20, v_pad), (180, 40)),
                                                                    playerWindow.aiPlayerNames[i] + ":  " + str(setupWindow.chip_count) + "  |  ",
                                                                    manager=manager,
                                                                    object_id="config_window_label",
                                                                    container=self,
                                                                    parent_element=self,
                                                                    anchors={
                                                                        "left": "left",
                                                                        "top_target": self.numplayer_label
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
            pygame.Rect((h_pad, v_pad), (200, 40)),
            initial_text=f"player{i+1}",  # Use f-string to include the player number in the initial text
            placeholder_text="Player Name",
            container=self,
            parent_element=self,
            anchors={"left": "left"}
            )
            player_name_label.set_text_length_limit(9),
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

        handled = super().process_event(event)

        if (event.type == pygame_gui.UI_BUTTON_PRESSED):
            if (event.ui_element == self.submit_button):
                self.player_name = [label.get_text() for label in self.player_name_labels]
                playerNames = self.player_name
                playScreen.playerNames = self.player_name
                playerNameSetUp.submitPlayerClicked = True
                self.kill()
                print(self.player_name)
                print(playerNames)
        playerNames = self.player_name

class betWindow(pygame_gui.elements.UIWindow):
    def __init__(self, manager, pos):
        super().__init__((pos),
                        manager,
                        window_display_title='BETTING_PLACEHOLDER',
                        object_id='#setup_window',
                        draggable=False)
        self.v_pad = 30
        self.h_pad = 30

        self.button_height = 40

        self.fold_button_width = (pos.width*.333)-self.h_pad
        #self.dynamic_button_width = pos.width-((self.h_pad*4)+self.fold_button_width)
        self.dynamic_button_width = pos.width*.666-self.h_pad*3

        self.yourmoney_label = pygame_gui.elements.UILabel(pygame.Rect((self.v_pad, self.h_pad), (pos.width, 40)),
                                                           "You have $CHIP_AMOUNT_HERE",
                                                           object_id="config_window_label",
                                                           container=self,
                                                           parent_element=self,
                                                           anchors={
                                                               "left": "left"
                                                           })
        self.bet_label = pygame_gui.elements.UILabel(pygame.Rect((self.v_pad, self.h_pad), (40, 40)),
                                                           "Bet:",
                                                           object_id="config_window_label",
                                                           container=self,
                                                           parent_element=self,
                                                           anchors={
                                                               "top_target": self.yourmoney_label,
                                                               "left": "left"
                                                           })
        self.bet_input_box = pygame_gui.elements.UITextEntryLine(pygame.Rect((self.h_pad, self.v_pad), (90, 40)),
                                                           placeholder_text="0",
                                                           container=self,
                                                           parent_element=self,
                                                           anchors={
                                                               "left_target": self.bet_label,
                                                               "top_target": self.yourmoney_label
                                                           })
        self.fold_button = pygame_gui.elements.UIButton(pygame.Rect((self.h_pad, -(self.v_pad+self.button_height)), (self.fold_button_width, self.button_height)),
                                                        "Fold",
                                                        manager=manager,
                                                        container=self,
                                                        parent_element=self,
                                                        anchors={
                                                            "bottom": "bottom",
                                                            "left": "left"
                                                        })
        self.dynamic_button = pygame_gui.elements.UIButton(pygame.Rect((self.h_pad, -(self.v_pad+self.button_height)), (self.dynamic_button_width, self.button_height)),
                                                           "Check",
                                                           manager=manager,
                                                           container=self,
                                                           parent_element=self,
                                                           anchors={
                                                               "bottom": "bottom",
                                                               "left": "left",
                                                               "left_target": self.fold_button
                                                           })
        
    def process_event(self, event):
        handled = super().process_event(event)

        if (event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED):
            if (event.ui_element == self.bet_input_box and self.bet_input_box.get_text() == "0"):
                self.dynamic_button.set_text("Check")
            elif (not self.bet_input_box.get_text() == "0"):
                self.dynamic_button.set_text("Bet")

class camWindow(pygame_gui.elements.UIWindow):
    def __init__(self, manager, pos):
        super().__init__((pos),
                        manager,
                        window_display_title='CAMERA_WINDOW',
                        object_id='#setup_window',
                        draggable=False)
        
        global drawcam
        
        imgsurf = pygame.Surface(size=(pos.width, pos.height))
        imgsurf.fill((0, 0, 0)) # black
        
        self.camera_display = pygame_gui.elements.UIImage(pygame.Rect((0, 0), (pos.width, pos.height)),
                                                          image_surface=imgsurf,
                                                          manager=manager,
                                                          container=self,
                                                          parent_element=self
                                                          )
        
        cameras = pygame.camera.list_cameras()
        self.webcam = pygame.camera.Camera(cameras[0])
        self.webcam.start()
    
    def draw_camera(self):
        global drawcam

        if drawcam and self.webcam.query_image():
            img = self.webcam.get_image()
            img = pygame.transform.flip(img, True, False) # fix horizontal flip
            self.camera_display.set_image(img)
            
class infoWindow(pygame_gui.elements.UIWindow):
    def __init__(self, manager, pos):
        super().__init__((pos),
                         manager,
                         window_display_title='How to Play Poker',
                         object_id='#info_window',
                         draggable=True)
        self.scroll_box = pygame_gui.elements.UIScrollingContainer(pygame.Rect((0, 0), (200, 200)),
                                                                                             manager=manager,
                                                                                             container=self,
                                                                                             object_id="scroll_container"
        )
        self.info_label = pygame_gui.elements.UILabel(pygame.Rect((0, 0), (200, 1)),
                                                      "",
                                                      manager=manager,
                                                      container=self.scroll_box,
                                                      object_id="info_label"
        )
    def load_text(self, file_path):
        try:
            with open(file_path, 'r') as file:
                text = file.read()
                self.info_label.set_text(text)
                self.scroll_box.set_dimensions((400, 400))
        except FileNotFoundError:
            print(f"File not found: {file_path}")

class churchWindow(pygame_gui.elements.UIWindow):
    def __init__(self, manager, pos):
        super().__init__((pos),
                         manager,
                         window_display_title='How to Donate!',
                         object_id='#church_window',
                         draggable=True)
        self.donation_label = pygame_gui.elements.UITextBox("Please click the button below to donate to our local church! We hope you enjoyed using xtcards :)",
                                                            relative_rect=pygame.Rect((0, 10), (300, 200)),
                                                            manager=manager,
                                                            container=self,
                                                            parent_element=self,
                                                            anchors={
                                                            "centerx": "centerx"
                                                            })
        self.donate_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((125, 300), ((100), 40)),
                                                          text='Donate',
                                                          manager=manager,
                                                          container=self,
                                                          parent_element=self,
                                                          anchors={
                                                              "bottom': 'bottom",
                                                              "centerx': 'centerx"
                                                          })
