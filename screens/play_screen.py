import pygame
import pygame_gui
from pygame_gui.elements import UILabel

from objects.screenstate import ScreenState
from objects.camstate import CameraState
from objects.scheme import Scheme

from windows.setup import setupWindow
from windows.pause_window import pauseWindow
from windows.player_window import playerWindow
from windows.bank_window import bankWindow
from windows.player_name_setup import playerNameSetupWindow
from windows.bet_window import betWindow
from windows.cam_window import camWindow
from windows.info_window import infoWindow
from windows.church_window import churchWindow

from game_logic.game import GameState
from game_logic.player import Player

import pygame.camera

# image proc
import cv2
import base64
import requests
import json
import numpy as np

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

        self.header = None
        self.camwindow = None
        self.betwindow = None

        self.camClicked = False
        self.betClicked = False # TEMP

        # Class variable for a new GameState from game_logic/game.py.
        # This variable is updated after number of players/AI is selected.

        # For future save game functions, this class variable should be loaded
        # from the saved game's GameState object.
        # (more on this functionality later)
        self.game_state = None

        self.cam_state = None

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

        # pause button
        pause_button_rect = pygame.Rect(15, 15, 100, 50)
        self.pause_button = pygame_gui.elements.UIButton(relative_rect=pause_button_rect,
                                            text='Pause',
                                            manager=manager,
                                            anchors={
                                            'left': 'left',
                                            'top': 'top'
                                            })
        self.pause_button.hide()

        # Scan AI cards button
        dealing_button_rect = pygame.Rect(15, -100, 250, 50)
        self.scan_button = pygame_gui.elements.UIButton(relative_rect=dealing_button_rect,
                                            text='Scan AI\'s Hand',
                                            manager=manager,
                                            anchors={
                                            'centerx': 'centerx',
                                            'bottom': 'bottom'
                                            })
        self.scan_button.hide()

        self.showbet_button = pygame_gui.elements.UIButton(relative_rect=pause_button_rect,
                                            text='betwin',
                                            manager=manager,
                                            anchors={
                                            'left': 'left',
                                            'top': 'top',
                                            'left_target': self.pause_button
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

        self.current_ai_card_scan = 0 # used to track which AI we need to persistently scan cards for
        self.ai_cards = []

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

        # cam set up
        cam_width = self.width*.4
        cam_height = self.height*.7
        campos = pygame.Rect(((self.width*.5)-(cam_width//2), self.height*.125), (cam_width, cam_height))

        # info icon set up
        info_width = self.width*.20
        info_height = self.height*.4
        infopos = pygame.Rect(((self.width)-(info_width+10), (self.height/2)-(info_height)), (info_width, info_height))

        # church icon set up
        church_width = self.width*.20
        church_height = self.height*.4
        churchpos = pygame.Rect(((self.width)-(church_width*3), (self.height/2)-(church_height/2)), (church_width, church_height))

        while True:
            time_delta = self.clock.tick(60) / 1000.0
            keys = pygame.key.get_pressed()

            # if setup window is closed, open player window and pause button
            if(setupWindow.startClicked):
                # show header
                self.header.show()
                self.playerSetUp = playerNameSetupWindow(manager, playerSetuppos, setupWindow.player_count)
                setupWindow.startClicked = False

            # START THE GAME
            if(playerNameSetupWindow.submitPlayerClicked):
                print("BEFORE: -----------" + str(len(self.playerSetUp.playerNames)) + "-----------")
                self.players = playerWindow(manager, playerspos, self.playerSetUp.playerNames, setupWindow.chip_count, setupWindow.ai_player_count)
                
                self.pause_button.show()
                self.showbet_button.show()
                
                self.header.set_text('Start Dealing Cards')
                self.scan_button.show()
                playerNameSetupWindow.submitPlayerClicked = False

                self.header.show()
                self.info_button.show()
                self.church_button.show()

                self.bank = bankWindow(manager=manager, pos=bankpos)

                setupWindow.startClicked = False # why is this here?

                # Process player/AI combo tuple
                # self.playerSetUp.playerNames - input player names
                # self.players.aiplayercount - selected AI count
                # self.players.aiPlayerNames - shuffled AI player names
                game_participants = []
                self.human_participants = []
                self.ai_participants = []
                chips = setupWindow.chip_count
                
                for player in self.playerSetUp.playerNames:
                    person = Player(name=player, is_ai=False, chips=chips)
                    self.human_participants.append(person)
                
                for i in range(self.players.aiplayercount):
                    ai = Player(name=self.players.aiPlayerNames[i], is_ai=True, chips=chips)
                    self.ai_participants.append(ai)
                    
                game_participants.append(self.human_participants)
                game_participants.append(self.ai_participants)
                
                self.game_state = GameState(game_participants) # // START GAME INSTANCE //
                self.cam_state = CameraState.SCAN_AI_HAND # begin the game by scanning the AI's cards

            for event in pygame.event.get():
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    # PAUSE BUTTON
                    if (event.ui_element == self.pause_button and not pauseClicked):
                            print('TITLE: Drawing pause dialog')
                            pauseClicked = True
                            self.pause = pauseWindow(manager=manager, pos=pausepos)
                            self.pause.set_blocking(True)
                    
                    # CAMERA BUTTON
                    if (event.ui_element == self.scan_button):
                        if (not self.camClicked):
                            print('OPENING CAM')
                            self.camwindow = camWindow(manager, campos)
                            self.camClicked = True
                            self.header.set_text('Scan AI Cards')
                        elif (self.camClicked):
                            print('KILLING CAM')
                            self.killCamera()
                    
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
                            self.info = infoWindow(manager=manager, pos=infopos)
                            self.info.set_blocking(False)
                            self.info.load_text("assets/poker_rules.txt")

                    # DONATION BUTTON
                    if (event.ui_element == self.church_button and not churchClicked):
                        print('TITLE: Drawing donation dialog')
                        churchClicked = True
                        self.church = churchWindow(manager=manager, pos=churchpos)
                        self.church.set_blocking(False)

                if event.type == pygame.QUIT:
                    return ScreenState.QUIT
                if keys[pygame.K_ESCAPE]:
                    print('DEBUG: Switching to TITLE')
                    homeswitch = True

                manager.process_events(event)

            # --------------------
            # GAME FLOW STATEMENTS
            # --------------------
            if (self.cam_state == CameraState.BETTING):
                self.scan_button.hide()

            if (self.cam_state == CameraState.SCAN_AI_HAND):
                if (self.camClicked):
                    curr_ai = self.players.aiPlayerNames[self.current_ai_card_scan]
                    self.scan_button.hide()

                    if not self.ai_cards: # no cards in ai hand list yet
                        self.camwindow.instruction_label.set_text( "%s's cards - 1 of 2" % (curr_ai) )

                    if (self.camwindow.snaptaken): # scan frame upon clicking button
                        card = self.scanCard()
                        self.ai_cards.append(card)

                        if (len(self.ai_cards) == 1):
                            self.camwindow.instruction_label.set_text( "%s's cards - 2 of 2" % (curr_ai) )

                        elif (self.current_ai_card_scan == self.players.aiplayercount-1): # see if we have no more AI to scan
                            # SEND SELF.AI_CARDS TO GAME FLOW HERE
                            print("AI CARDS:")
                            print(self.ai_cards) # for now just print
                            self.ai_cards = []
                            self.current_ai_card_scan = self.current_ai_card_scan + 1

                            self.killCamera()
                            self.cam_state = CameraState.BETTING

                        else:
                            # SEND SELF.AI_CARDS TO GAME FLOW HERE (the same as above)
                            print("AI CARDS:")
                            print(self.ai_cards) # for now just print
                            self.ai_cards = []
                            self.current_ai_card_scan = self.current_ai_card_scan + 1

            if (self.cam_state == CameraState.SCAN_FLOP):
                self.scan_button.show()

            manager.update(time_delta)
            self.window.blit(self.background, (0,0))
            
            if self.camwindow != None:
                self.camwindow.draw_camera()

            manager.draw_ui(self.window)

            # Check and reset flags
            if (pauseClicked):
                if not self.pause.alive():
                    pauseClicked = False
                if self.pause.homeswitch:
                    self.pause.homeswitch = False
                    homeswitch = True
            
            if (infoClicked):
                if not self.info.alive():
                    infoClicked = False
            if (churchClicked):
                if not self.church.alive():
                    churchClicked = False

            pygame.display.update()

            if (homeswitch):
                if (self.camwindow != None):
                    self.killCamera()
                self.state = ScreenState.TITLE
                homeswitch = False
            if (self.state != ScreenState.START):
                return self.state

    def delete(self, manager):
        print('DEBUG: Deleting objects')
        manager.clear_and_reset()
    
    def killCamera(self):
        # only call if self.camwindow != None
        self.camwindow.drawcam = False
        self.camClicked = False
        self.camwindow.webcam.release()
        self.camwindow.kill()
        self.camwindow = None
    
    def scanCard(self):
        card = self.sendImg(self.camwindow.img) # send lambda call
        self.camwindow.snaptaken = False
        self.camwindow.drawcam = True

        return card
    
    def sendImg(self, img):
        # send img to AWS lambda, store res
        # used to scan AI / player cards
        img = cv2.resize(img, dsize=(224, 224), interpolation=cv2.INTER_CUBIC)
        img = np.array(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        img_bytes = img.tobytes()
        img_b64 = base64.b64encode(img_bytes).decode('utf-8')

        response = requests.post('https://ml-api.kailauapps.com/card-detection', json={'b64img': str(img_b64)})
        response = json.loads(response.text)
        
        return response["class"]
