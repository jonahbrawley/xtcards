import pygame
import pygame_gui
from objects.gamestate import GameState
from objects.scheme import Scheme

class setupWindow(pygame_gui.elements.UIWindow):
    def __init__(self, manager, pos):
        super().__init__((pos),
                         manager,
                         window_display_title='Game Setup',
                         object_id='#config_window')
        
        player_selection = ["2", "3", "4"]

        self.numplayer_label = pygame_gui.elements.UILabel(pygame.Rect((10, 10), (180, 40)),
                                                                "Number of players?",
                                                                manager=manager,
                                                                object_id="config_window_label",
                                                                container=self,
                                                                parent_element=self,
                                                                anchors={
                                                                    "left": "left"
                                                                })
        
        self.players_dropdown = pygame_gui.elements.UIDropDownMenu(options_list=player_selection,
                                                                   starting_option="2",
                                                                   relative_rect=pygame.Rect((10, 10), (70, 40)),
                                                                   manager=manager,
                                                                   container=self,
                                                                   parent_element=self,
                                                                   anchors={
                                                                       "left_target": self.numplayer_label
                                                                   })