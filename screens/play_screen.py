import pygame
import pygame_gui

from pygame_gui.elements import UILabel
from objects.screenstate import ScreenState
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

import pygame.camera

homeswitch = False

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

        self.header = None
        self.camwindow = None
        self.betwindow = None

        self.camClicked = False # TEMP
        self.betClicked = False # TEMP

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
            time_delta = self.clock.tick(60) / 1000.0
            keys = pygame.key.get_pressed()

            # if setup window is closed, open player window and pause button
            if(setupWindow.startClicked):
                # show header
                self.header.show()
                self.playerSetUp = playerNameSetupWindow(manager, playerSetuppos, setupWindow.player_count)
                setupWindow.startClicked = False

            if(playerNameSetupWindow.submitPlayerClicked):
                print("BEFORE: -----------" + str(len(self.playerSetUp.playerNames)) + "-----------")
                #player widnow
                self.players = playerWindow(manager, playerspos, self.playerSetUp.playerNames, setupWindow.chip_count, setupWindow.ai_player_count)
                # show pause button
                self.pause_button.show()

                self.showcam_button.show()
                self.showbet_button.show()
                # hide header
                self.header.hide()
                #build bank
                self.bank = bankWindow(manager=manager, pos=bankpos)
                playerNameSetupWindow.submitPlayerClicked = False
                self.header.show()
                #show info button
                self.info_button.show()
                #show donation button
                self.church_button.show()
                self.bank = bankWindow(manager=manager, pos=bankpos)
                setupWindow.startClicked = False

            for event in pygame.event.get():
                #if pause button is clicked
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if (event.ui_element == self.pause_button and not pauseClicked):
                            print('TITLE: Drawing pause dialog')
                            pauseClicked = True
                            self.pause = pauseWindow(manager=manager, pos=pausepos)
                            self.pause.set_blocking(True)
                    
                    if (event.ui_element == self.showcam_button):
                        if (not self.camClicked):
                            print('OPENING CAM')
                            self.camwindow = camWindow(manager, campos)
                            self.camClicked = True
                        elif (self.camClicked):
                            print('KILLING CAM')
                            self.camwindow.drawcam = False
                            self.camClicked = False
                            self.camwindow.webcam.stop()
                            self.camwindow.kill()
                            self.camwindow = None
                    
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
                    

                    #if info button clicked
                    if (event.ui_element == self.info_button and not infoClicked):
                            print('TITLE: Drawing info dialog')
                            infoClicked = True
                            self.info = infoWindow(manager=manager, pos=infopos)
                            self.info.set_blocking(False)
                            self.info.load_text("assets/poker_rules.txt")

                    #if donation button clicked
                    if (event.ui_element == self.church_button and not churchClicked):
                        print('TITLE: Drawing donation dialog')
                        churchClicked = True
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
                self.camwindow.drawcam = True
                self.camwindow.draw_camera()

            manager.draw_ui(self.window)
            
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
                self.state = ScreenState.TITLE
                homeswitch = False

            if (self.state != ScreenState.START):
                return self.state
    
    def delete(self, manager):
        print('DEBUG: Deleting objects')
        manager.clear_and_reset()
