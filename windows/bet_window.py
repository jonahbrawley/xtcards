import pygame
import pygame_gui

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