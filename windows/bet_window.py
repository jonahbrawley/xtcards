import pygame
import pygame_gui
from game_logic.game import GameInstance

min_req_bet = "0" 
class betWindow(pygame_gui.elements.UIWindow):
    def __init__(self, manager, pos, min_bet):
        super().__init__((pos),
                        manager,
                        window_display_title='What do you wager?',
                        object_id='#setup_window',
                        draggable=False)
        self.v_pad = 30
        self.h_pad = 30

        min_req_bet = str(min_bet)

        self.placed_bet = None # starts with no bet
        self.folds = False # set to True if they fold

        self.initial_bet = "0"
        self.bet_input_box = min_bet

        if (self.bet_input_box > 0):
            self.initial_bet = str(self.bet_input_box)

        self.button_height = 40

        self.fold_button_width = (pos.width*.333)-self.h_pad
        
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
                                                        initial_text= self.initial_bet,
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
                                                        "Check/Call",
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
            if (event.ui_element == self.bet_input_box and (self.bet_input_box.get_text() == "0" or self.bet_input_box.get_text() == min_req_bet)):
                self.dynamic_button.set_text("Check/Call")
            elif (not self.bet_input_box.get_text() == "0"):
                self.dynamic_button.set_text("Raise")
        if (event.type == pygame_gui.UI_BUTTON_PRESSED):
            if (event.ui_element == self.dynamic_button):
                self.placed_bet = self.bet_input_box.get_text()
            if (event.ui_element == self.fold_button):
                self.folds = True