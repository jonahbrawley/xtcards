import pygame
import pygame_gui

class setupWindow(pygame_gui.elements.UIWindow):
    def __init__(self, manager, pos):
        super().__init__((pos),
                         manager,
                         window_display_title='Game Setup',
                         object_id='#setup_window',
                         draggable=False)
        
        player_selection = ["1", "2", "3"]
        ai_selection = ["1", "2", "3"]

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