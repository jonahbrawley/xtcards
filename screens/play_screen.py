import pygame
import pygame_gui
from pygame_gui.elements import UILabel
from pygame_gui.elements import UITextBox

from objects.screenstate import ScreenState
from objects.gamestate import GameState
from objects.scheme import Scheme
from windows.results_window import resultsWindow

from windows.setup import setupWindow
from windows.pause_window import pauseWindow
from windows.player_window import playerWindow
from windows.bank_window import bankWindow
from windows.log_window import logWindow
from windows.table_window import tableWindow
from windows.player_name_setup import playerNameSetupWindow
from windows.bet_window import betWindow
from windows.cam_window import camWindow
from windows.info_window import infoWindow
from windows.church_window import churchWindow

from game_logic.game import GameInstance
from game_logic.player import Player

from local_ml.card_detection import classify_card

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
        self.offload_card_detection = True
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

        # Class variable for a new GameInstance from game_logic/game.py.
        # This variable is updated after number of players/AI is selected.

        # For future save game functions, this class variable should be loaded
        # from the saved game's GameInstance object.
        # (more on this functionality later)
        self.game_instance = None

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

        # end round button
        dealing_button_rect = pygame.Rect(15, -100, 250, 50)
        self.scan_button = pygame_gui.elements.UIButton(relative_rect=dealing_button_rect,
                                            text='Scan AI\'s Hand',
                                            manager=manager,
                                            anchors={
                                            'centerx': 'centerx',
                                            'bottom': 'bottom'
                                            })
        self.scan_button.hide()

        # info button
        info_button_rect = pygame.Rect(-55, 15, 40, 50)
        self.info_button = pygame_gui.elements.UIButton(relative_rect=info_button_rect,
                                                text='i',
                                                manager=manager,
                                                anchors={
                                                'right': 'right'
                                                })
        self.info_button.hide()

        # donation button
        church_button_rect = pygame.Rect(-415, 15, 350, 50)
        self.church_button = pygame_gui.elements.UIButton(relative_rect=church_button_rect,
                                                        text='DONATE TO MAGNOLIA CHURCH',
                                                        object_id='#church_button',
                                                        manager=manager,
                                                        anchors={
                                                        'right': 'right'
                                                        })
        self.church_button.hide()

        self.player_index = 0 # keep track of which player we are operating on
        self.card_index = 0 # which card are we scanning
        self.cards_scanned = []


        # bet set up TEMP
        result_width = self.width*.3
        result_height = self.height*.22
        results_rect = pygame.Rect(((self.width*.50)-(result_width//2), self.height/1.8), (result_width, result_height))

        self.result_text = UITextBox(' ',
                            relative_rect=results_rect,
                            manager=manager,
                            object_id='result_textbox',
                            anchors={
                                'left': 'left',
                                'top': 'top'
                            })
        self.result_text.hide()

        self.setup = setupWindow(manager, stppos)

    def run(self, manager):
        global homeswitch
        pauseClicked = False
        infoClicked = False
        churchClicked = False
        logClicked = False

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
        bank_height = self.height*.275
        bankpos = pygame.Rect((self.width - (bank_width+10), self.height-(bank_height+10)), (bank_width, bank_height))
        
        # log set up
        log_width = self.width*.25
        log_height = self.height*.275
        logpos = pygame.Rect((self.width - (log_width+10), self.height-(log_height*3)), (log_width, log_height))

        # table set up
        tablepos = pygame.Rect((self.width - (bank_width+10), self.height-((bank_height*2)+10)), (bank_width, bank_height))
        resultpos = pygame.Rect(((self.width/2)-(self.width*.3/2), (self.height/2.8)-(bank_height/2)), (self.width*.3, bank_height))

        # player name set up
        playerSetup_width = self.width*.26
        playerSetup_height = self.height*.46
        playerSetuppos = pygame.Rect(((self.width/2)-(playerSetup_width/2), (self.height/2)-(playerSetup_height/2)), (playerSetup_width, playerSetup_height))

        # bet set up
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
        infopos = pygame.Rect(((self.width)-(info_width+10), (self.height/2.15)-(info_height)), (info_width, info_height))

        # church icon set up
        church_width = self.width*.2
        church_height = self.height*.45
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
                #print("BEFORE: -----------" + str(len(self.playerSetUp.playerNames)) + "-----------")
                self.players = playerWindow(manager, playerspos, self.playerSetUp.playerNames, setupWindow.chip_count, setupWindow.ai_player_count)
                self.pause_button.show()
                playerNameSetupWindow.submitPlayerClicked = False

                self.header.show()
                self.info_button.show()
                self.church_button.show()

                self.table = tableWindow(manager=manager, pos=tablepos)
                self.result_table = resultsWindow(manager=manager, pos=resultpos)
                self.result_table.hide()
                self.bank = bankWindow(manager=manager, pos=bankpos)
                self.log = logWindow(manager=manager, pos=logpos)
                self.log.hide()
            
                self.bank.show_log = False
                setupWindow.startClicked = False

                if (self.bank.show_log == True):
                    self.log.show()

                # Process player/AI combo tuple
                # self.playerSetUp.playerNames - input player names
                # self.players.aiplayercount - selected AI count
                # self.players.aiPlayerNames - shuffled AI player names
                game_participants = []
                chips = setupWindow.chip_count
                curr_id = 0
                
                for player in self.playerSetUp.playerNames:
                    person = Player(name=player, is_ai=False, chips=chips, id=curr_id)
                    game_participants.append(person)
                    curr_id += 1
                
                for i in range(self.players.aiplayercount):
                    ai = Player(name=self.players.aiPlayerNames[i], is_ai=True, chips=chips, id=curr_id)
                    game_participants.append(ai)
                    curr_id += 1

                # update chips for player window
                self.game_instance = GameInstance(game_participants) # // START GAME INSTANCE //
                self.game_state = GameState.SCAN_AI_HAND # begin the game by scanning the AI's cards

            for event in pygame.event.get():
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if (event.ui_element == self.pause_button and not pauseClicked): # PAUSE BUTTON
                            print('PLAY: Drawing pause dialog')
                            pauseClicked = True
                            self.pause = pauseWindow(manager=manager, pos=pausepos)
                            self.pause.set_blocking(True)

                    if (event.ui_element == self.info_button and not infoClicked): # INFO BUTTON
                            print('PLAY: Drawing info dialog')
                            infoClicked = True
                            self.info = infoWindow(manager=manager, pos=infopos)
                            self.info.set_blocking(False)

                    if (event.ui_element == self.church_button and not churchClicked): # DONATION BUTTON
                        print('PLAY: Drawing donation dialog')
                        churchClicked = True
                        self.church = churchWindow(manager=manager, pos=churchpos)
                        self.church.set_blocking(False)

                if event.type == pygame.QUIT:
                    return ScreenState.QUIT
                if keys[pygame.K_ESCAPE]:
                    print('PLAY: Switching to TITLE')
                    self.killCamera()
                    self.killGame()
                    homeswitch = True

                manager.process_events(event)

            # --------------------
            # GAME FLOW STATEMENTS
            # --------------------
            if (self.game_state == GameState.SCAN_AI_HAND):
                self.header.set_text('Scan AI Cards')

                if (self.camClicked):
                    cards_to_scan = 2

                    while (self.player_index < len(self.game_instance.players) and not self.game_instance.players[self.player_index].is_ai):
                        self.player_index += 1
                    
                    if (self.player_index < len(self.game_instance.players)):
                        curr_player = self.game_instance.players[self.player_index]
                        
                        self.camwindow.instruction_label.set_text( "%s's cards - %d of 2" % (curr_player.name, self.card_index+1) )

                        if (self.camwindow.snaptaken):
                            self.cards_scanned.append(self.scanCard())
                            self.card_index += 1
                        
                        if (self.card_index >= cards_to_scan):
                            self.card_index = 0
                            curr_player.cards = self.cards_scanned
                            self.cards_scanned = []
                            self.player_index += 1
                    else: # done scanning cards
                        self.camwindow.scanning_ai_cards = False
                        self.player_index = 0
                        self.card_index = 0
                        self.cards_scanned = []

                        self.game_instance.start_game()
                        self.game_instance.step() # perform small and big blinds
                        self.killCamera()
                        self.game_state = GameState.PREFLOP_BETS
                else:
                    self.viewCamera(manager, campos) # open camera window
                    self.camwindow.scanning_ai_cards = True # hide AI cards from player

            player_blinds = {}
            if (self.game_state == GameState.PREFLOP_BETS or self.game_state == GameState.POST_FLOP_BETS or 
                self.game_state == GameState.POST_TURN_BETS or self.game_state == GameState.FINAL_BETS):
                # get the current player details with
                player_pos = self.game_instance.curr_pos
                player_action_label = self.players.player_action_list[player_pos]
                player_label = self.players.player_labels_list[player_pos]
                if (self.game_state == GameState.PREFLOP_BETS and player_blinds == {}): 
                    player_blinds = self.game_instance.tmp_pot.bets
                    for player_index, blind_value in player_blinds.items():
                        #print(self.players.player_action_list)
                        #print(player_blinds.items())
                        self.players.player_action_list[player_index].set_text(str(blind_value))
                        # player_label.set_text(self.game_instance.players[player_index].name + ":  " + str(self.game_instance.players[player_index].chips) + "  |  ")

                next_state = GameState.UNCHANGED_STATE
                

                player = self.game_instance.players[self.game_instance.curr_pos].name # returns Player instance from player.py
                # show bet dialogue & collect input action, bet for that player
                self.header.set_text(player + "'s Turn")
                self.min_bet = self.game_instance.get_min_required_bet()

                if (self.betwindow == None):
                    self.betwindow = betWindow(manager, betpos, self.min_bet)
                    self.betwindow.yourmoney_label.set_text("You have " + str(self.game_instance.players[self.game_instance.curr_pos].chips) + " chips")
                    print('PLAY: Drawing bet window')
                else: # bet window open
                    if (self.betwindow.folds):
                        self.betwindow.kill()
                        self.betwindow = None
                        next_state = self.game_instance.step('fold')
                        player_action_label.set_text("folded")

                    elif (self.betwindow.placed_bet != None):
                        #print(self.game_instance)
                        if (self.betwindow.placed_bet == "0"):
                            next_state = self.game_instance.step('call', int(self.betwindow.placed_bet))
                            player_action_label.set_text("Check")
                        elif (int(self.betwindow.placed_bet) <= self.min_bet):
                            next_state = self.game_instance.step('call', int(self.betwindow.placed_bet))
                            player_action_label.set_text(self.betwindow.placed_bet)
                        else:
                            # print('Player bet ' + self.betwindow.placed_bet + " chips")
                            player_action_label.set_text(self.betwindow.placed_bet)
                            next_state = self.game_instance.step('raise', int(self.betwindow.placed_bet))
                        # current player's chips
                        self.player_chips = self.game_instance.players[player_pos].chips
                        player_label.set_text(player + ":  " + str(self.player_chips) + "  |  ")
                        #self.updateGameLog(self.players.player_action_list)

                        self.betwindow.kill()
                        self.betwindow = None

                if  next_state == GameState.SCAN_FLOP:
                    self.bank.value_label.set_text(str(self.game_instance.get_total_pot_value()))
                    for players in self.players.player_action_list:
                        players.set_text('')
                    self.game_state = GameState.SCAN_FLOP
                    self.header.set_text('Scan Flop')

                if  next_state == GameState.SCAN_TURN:   
                    self.bank.value_label.set_text(str(self.game_instance.get_total_pot_value()))
                    for players in self.players.player_action_list:
                        players.set_text('')
                    self.game_state = GameState.SCAN_TURN
                    self.header.set_text('Scan Turn Card')

                if  next_state == GameState.SCAN_RIVER:
                    self.bank.value_label.set_text(str(self.game_instance.get_total_pot_value()))
                    for players in self.players.player_action_list:
                        players.set_text('')
                    self.game_state = GameState.SCAN_RIVER
                    self.header.set_text('Scan River Card')

                if  next_state == GameState.SCAN_PLAYER_HAND:
                    self.bank.value_label.set_text(str(self.game_instance.get_total_pot_value()))
                    for players in self.players.player_action_list:
                        players.set_text('')
                    self.game_state = GameState.SCAN_PLAYER_HAND
                    self.player_index = 0
                    self.card_index = 0
                    self.header.set_text('Scan Player Hands')

            if (self.game_state == GameState.SCAN_FLOP):
                if (self.camClicked):
                    cards_to_scan = 3

                    if (self.card_index < cards_to_scan):
                        self.camwindow.instruction_label.set_text( "Scan flop - %d of 3" % (self.card_index+1) )

                        if (self.camwindow.snaptaken):
                            card = self.scanCard()
                            self.game_instance.community_cards[self.card_index] = card
                            self.updateTable(self.game_instance.community_cards) # update the table
                            self.card_index += 1
                    if (self.card_index == cards_to_scan):
                        self.killCamera()
                        print(self.game_instance.community_cards)
                        self.game_state = GameState.POST_FLOP_BETS
                else:
                    self.viewCamera(manager, campos) # open camera window

            if (self.game_state == GameState.SCAN_TURN):
                if (self.camClicked):
                    cards_to_scan = 4

                    if (self.card_index < cards_to_scan):
                        self.camwindow.instruction_label.set_text( "Scan turn - %d of 1" % (self.card_index+1-3) )

                        if (self.camwindow.snaptaken):
                            card = self.scanCard()
                            self.game_instance.community_cards[self.card_index] = card
                            self.updateTable(self.game_instance.community_cards) # update the table
                            self.card_index += 1
                    if (self.card_index == cards_to_scan):
                        self.killCamera()
                        print(self.game_instance.community_cards)
                        self.game_state = GameState.POST_TURN_BETS
                else:
                    self.viewCamera(manager, campos) # open camera window

            if (self.game_state == GameState.SCAN_RIVER):
                if (self.camClicked):
                    cards_to_scan = 5

                    if (self.card_index < cards_to_scan):
                        self.camwindow.instruction_label.set_text( "Scan river - %d of 1" % (self.card_index+1-4) )

                        if (self.camwindow.snaptaken):
                            card = self.scanCard()
                            self.game_instance.community_cards[self.card_index] = card
                            self.updateTable(self.game_instance.community_cards) # update the table
                            self.card_index += 1
                    if (self.card_index == cards_to_scan):
                        self.card_index = 0
                        self.killCamera()
                        print(self.game_instance.community_cards)
                        self.game_state = GameState.FINAL_BETS
                else:
                    self.viewCamera(manager, campos) # open camera window

            if (self.game_state == GameState.SCAN_PLAYER_HAND):
                if (self.camClicked):
                    self.camwindow.scanning_ai_cards = False
                    cards_to_scan = 2

                    while (self.player_index < len(self.game_instance.players) and self.game_instance.players[self.player_index].is_ai):
                        self.player_index += 1
                    
                    if (self.player_index < len(self.game_instance.players)):
                        curr_player = self.game_instance.players[self.player_index]
                        
                        self.camwindow.instruction_label.set_text( "%s's cards - %d of 2" % (curr_player.name, self.card_index+1) )

                        if (self.camwindow.snaptaken):
                            self.cards_scanned.append(self.scanCard())
                            self.card_index += 1
                        
                        if (self.card_index >= cards_to_scan):
                            self.card_index = 0
                            print("PLAYER %s CARDS:" % (curr_player.name))
                            curr_player.cards = self.cards_scanned
                            self.game_instance.players[self.player_index].cards = curr_player.cards
                            print(curr_player.cards)
                            self.cards_scanned = []
                            self.player_index += 1
                    else: 
                        self.player_index = 0
                        self.card_index = 0
                        self.cards_scanned = []

                        self.killCamera()
                        self.game_state = GameState.END_ROUND # ready for reveal
                        rankings, results = self.game_instance.end_game()
                else:
                    self.viewCamera(manager, campos) # open camera window

            if (self.game_state == GameState.END_ROUND):
                self.result_text.show()
                self.scan_button.set_text('Next Round')
                self.scan_button.show()
                if (len(results) >= 2):
                    text = 'Split pot: '
                    winning_hand = rankings[0][0][2]
                    for position, chips in results.items():
                        player = self.game_instance.players[position]
                        text += f"{player.name} wins {chips} chips, "
                        self.player_chips = player.chips
                        player_label = self.players.player_labels_list[position]
                        player_label.set_text(player.name + ":  " + str(self.player_chips) + "  |  ")
                    self.result_text.set_text(text[:-2] + "\nTop Hand: " + winning_hand + "\n") 
                    self.header.set_text('Split Pot!')
                else:
                    winning_hand = rankings[0][0][2]
                    for position, chips in results.items():
                        player = self.game_instance.players[position]
                        self.result_text.set_text(f"{player.name} wins {chips} chips.\nTop Hand: {winning_hand}")
                        self.header.set_text(f"{player.name} wins {chips} chips!")
                        self.player_chips = player.chips
                        player_label = self.players.player_labels_list[position]
                        player_label.set_text(player.name + ":  " + str(self.player_chips) + "  |  ")
                for index in range(len(rankings[0][0][3])):
                    card = rankings[0][0][3][index]
                    if card != 'NA':
                        if card[1] == "H":
                            suit = "assets/cards/hearts"
                        elif card[1] == "D":
                            suit = "assets/cards/diamonds"
                        elif card[1] == "C":
                            suit = "assets/cards/clubs"
                        elif card[1] == "S":
                            suit = "assets/cards/spades"
                        if card[0] == "T":
                            id = suit + "/10.png"
                        else:
                            id = suit + "/" + card[0] + ".png"
                    card_element = getattr(self.result_table, f"card{index + 1}")
                    card_element.set_image(pygame.image.load(id))
                self.result_table.show()
                if (self.scan_button.pressed):
                    self.game_state = GameState.SCAN_AI_HAND
                    self.result_text.hide()
                    self.scan_button.hide()
                    self.result_table.hide()
                    self.clearTable(manager, tablepos)


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
            # if (logClicked):
            #     if not self.log.alive():
            #         logClicked = False

            pygame.display.update()

            if (homeswitch):
                if (self.camwindow != None):
                    self.killCamera()
                self.state = ScreenState.TITLE
                homeswitch = False
            if (self.state != ScreenState.START):
                return self.state

    def delete(self, manager):
        print('PLAY: Deleting objects')
        manager.clear_and_reset()

    def viewCamera(self, manager, pos):
        self.camwindow = camWindow(manager, pos)
        self.camClicked = True
    
    def killCamera(self):
        # only call if self.camwindow != None
        if (self.camwindow != None):
            self.camwindow.drawcam = False
            self.camwindow.webcam.release()
            self.camwindow.kill()
        self.camClicked = False
        self.camwindow = None
    
    def scanCard(self):
        card = self.sendImg(self.camwindow.img) # send lambda call
        self.camwindow.snaptaken = False
        self.camwindow.drawcam = True

        return card
    
    def sendImg(self, img):
        img = cv2.resize(img, dsize=(224, 224), interpolation=cv2.INTER_CUBIC)
        img = np.array(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        if self.offload_card_detection:
            # offloaded card detection ai
            response = classify_card(img)
            return response
        else:
            img_bytes = img.tobytes()
            img_b64 = base64.b64encode(img_bytes).decode('utf-8')

            response = requests.post('https://ml-api.kailauapps.com/card-detection', json={'b64img': str(img_b64)})
            response = json.loads(response.text)
            
            return response["class"]
        
    def clearTable(self, manager, tablepos):
        self.table.kill()
        self.table = None
        self.table = tableWindow(manager=manager, pos=tablepos)

    def updateTable(self, community_cards):
        suit = None
        id = None
        for index in range(len(community_cards)):
            card = community_cards[index]
            if card != 'NA':
                if card[1] == "H":
                    suit = "assets/cards/hearts"
                elif card[1] == "D":
                    suit = "assets/cards/diamonds"
                elif card[1] == "C":
                    suit = "assets/cards/clubs"
                elif card[1] == "S":
                    suit = "assets/cards/spades"
                
                if card[0] == "T":
                    id = suit + "/10.png"
                else:
                    id = suit + "/" + card[0] + ".png"
            
                card_element = getattr(self.table, f"card{index + 1}")
                card_element.set_image(pygame.image.load(id))
                #print("Table card " + str(index+1) + " set to " + id)

            index = index + 1
        #print("-- Done updating --")
        
    def updateGameLog(self):
        action_list = playerWindow.player_action_list
        labels = playerWindow.player_labels_list
        
        current_player = action_list[self.player_index]
        current_label = labels[self.player_index]
        log_text = f"{current_label.text} {current_player}"
        logWindow.game_log.set_text(log_text)

    def killGame(self):
        self.game_state = None
        self.player_index = 0
        self.card_index = 0
        self.game_instance = None
        Player.id = 0
        self.players = None