import pygame
import pygame_gui


class setupWindow(pygame_gui.elements.UIWindow):
    startClicked = False
    player_count = 1
    ai_player_count = 1
    chip_count = 200
    def __init__(self, manager, pos):
        super().__init__((pos),
                         manager,
                         window_display_title='Game Setup',
                         object_id='#setup_window',
                         draggable=False)
        
        player_selection = ["1", "2", "3", "4"]
        ai_selection = ["1", "2"]
        money_selection = ["100", "200", "300", "400", "500"]

        v_pad = 30
        h_pad = 30

        self.numplayer_label = pygame_gui.elements.UILabel(pygame.Rect((h_pad, v_pad), (180, 40)),
                                                                "Number of players?",
                                                                manager=manager,
                                                                object_id="config_window_label",
                                                                container=self,
                                                                parent_element=self,
                                                                anchors={
                                                                    "left": "left"
                                                                })
        
        self.players_dropdown = pygame_gui.elements.UIDropDownMenu(options_list=player_selection,
                                                                   starting_option="1",
                                                                   relative_rect=pygame.Rect((h_pad, v_pad), (70, 40)),
                                                                   manager=manager,
                                                                   container=self,
                                                                   parent_element=self,
                                                                   anchors={
                                                                       "left_target": self.numplayer_label
                                                                   })
        
        self.numai_label = pygame_gui.elements.UILabel(pygame.Rect((h_pad, 10), (180, 40)),
                                                                "Number of AI?",
                                                                manager=manager,
                                                                object_id="config_window_label",
                                                                container=self,
                                                                parent_element=self,
                                                                anchors={
                                                                    "left": "left",
                                                                    "top_target": self.numplayer_label
                                                                })
        
        self.ai_dropdown = pygame_gui.elements.UIDropDownMenu(options_list=ai_selection,
                                                                   starting_option="1",
                                                                   relative_rect=pygame.Rect((h_pad, 10), (70, 40)),
                                                                   manager=manager,
                                                                   container=self,
                                                                   parent_element=self,
                                                                   anchors={
                                                                       "left_target": self.numai_label,
                                                                       "top_target": self.players_dropdown
                                                                   })
        
        self.divider = pygame_gui.elements.UIProgressBar(pygame.Rect((h_pad-10, v_pad), ((pos.w-80), 5)),
                                                         manager=manager,
                                                         container=self,
                                                         parent_element=self,
                                                         anchors={
                                                             "top_target": self.numai_label,
                                                             "left": "left"
                                                         })
        
        self.player_money_label = pygame_gui.elements.UILabel(pygame.Rect((h_pad, 30), (180, 40)),
                                                                "Starting amount:",
                                                                manager=manager,
                                                                object_id="config_window_label",
                                                                container=self,
                                                                parent_element=self,
                                                                anchors={
                                                                    "left": "left",
                                                                    "top_target": self.divider
                                                                })
        
        self.player_money_dropdown = pygame_gui.elements.UIDropDownMenu(options_list=money_selection,
                                                                   starting_option="200",
                                                                   relative_rect=pygame.Rect((h_pad, 30), (70, 40)),
                                                                   manager=manager,
                                                                   container=self,
                                                                   parent_element=self,
                                                                   anchors={
                                                                       "left_target": self.player_money_label,
                                                                       "top_target": self.divider
                                                                   })
        
        # self.small_blind_label = pygame_gui.elements.UILabel(pygame.Rect((h_pad, 10), (180, 40)),
        #                                                         ("Small blind:"),
        #                                                         manager=manager,
        #                                                         object_id="config_window_label",
        #                                                         container=self,
        #                                                         parent_element=self,
        #                                                         anchors={
        #                                                             "left": "left",
        #                                                             "top_target": self.player_money_dropdown
        #                                                         })
        
        # self.big_blind_label = pygame_gui.elements.UILabel(pygame.Rect((h_pad, 10), (180, 40)),
        #                                                         ("Big blind:"),
        #                                                         manager=manager,
        #                                                         object_id="config_window_label",
        #                                                         container=self,
        #                                                         parent_element=self,
        #                                                         anchors={
        #                                                             "left": "left",
        #                                                             "top_target": self.small_blind_label
        #                                                         })

        self.start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, -60), ((160), 40)),
                                                             text='Start game',
                                                             manager=manager,
                                                             container=self,
                                                             parent_element=self,
                                                             anchors={
                                                                 "bottom": "bottom",
                                                                 "centerx": "centerx"
                                                             })

        # self.divider_label = pygame_gui.elements.UILabel(pygame.Rect((20, 10), (500, 50)),
        #                                                  "__________________________________________",
        #                                                  manager=manager,
        #                                                  object_id="config_window_label",
        #                                                  container=self,
        #                                                  parent_element=self,
        #                                                  anchors={
        #                                                      "left": "left",
        #                                                       "top_target": self.numai_label
        #                                                 })

    def process_event(self, event):

        handled = super().process_event(event)

        if (event.type == pygame_gui.UI_BUTTON_PRESSED):
            if (event.ui_element == self.start_button):
                setupWindow.player_count = int(self.players_dropdown.selected_option)
                setupWindow.ai_player_count = int(self.ai_dropdown.selected_option)
                setupWindow.chip_count = int(self.player_money_dropdown.selected_option)
                setupWindow.startClicked = True
                self.kill()