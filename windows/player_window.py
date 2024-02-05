import pygame
import pygame_gui

from random import shuffle

class playerWindow(pygame_gui.elements.UIWindow):
    aiPlayerNames = ["HolyBot", "AngelAI", "GodBot", "NoahsAI"]
    shuffle(aiPlayerNames)
    def __init__(self, manager, pos, playernames, chipcount, aiplayercount):
        self.playernames = playernames
        self.chipcount = chipcount
        self.aiplayercount = aiplayercount
        
        self.players_label = None
        
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
        self.player_action_list = []
        for i in range(len(self.playernames)):
            self.players_label = pygame_gui.elements.UILabel(pygame.Rect((20, v_pad), (180, 40)),
                                                                    self.playernames[i]+ ":  " + str(self.chipcount) + "  |  ",
                                                                    manager=manager,
                                                                    object_id="config_window_label",
                                                                    container=self,
                                                                    parent_element=self,
                                                                    anchors={
                                                                        "left": "left",
                                                                        "top_target": self.numplayer_label
                                                                    })
            self.player_labels_list.append(self.players_label)
            self.players_action = pygame_gui.elements.UILabel(pygame.Rect((180, v_pad), (180, 40)),
                                                                    "  ",
                                                                    manager=manager,
                                                                    object_id="config_window_label",
                                                                    container=self,
                                                                    parent_element=self,
                                                                    anchors={
                                                                        "left": "left",
                                                                        "top_target": self.numplayer_label
                                                                    })
            self.player_action_list.append(self.players_action)
            v_pad += 50
        for i in range(self.aiplayercount):
            self.ai_players_label = pygame_gui.elements.UILabel(pygame.Rect((20, v_pad), (180, 40)),
                                                                    playerWindow.aiPlayerNames[i] + ":  " + str(self.chipcount) + "  |  ",
                                                                    manager=manager,
                                                                    object_id="config_window_label",
                                                                    container=self,
                                                                    parent_element=self,
                                                                    anchors={
                                                                        "left": "left",
                                                                        "top_target": self.numplayer_label
                                                                    })
            self.player_labels_list.append(self.players_label)
            self.players_action = pygame_gui.elements.UILabel(pygame.Rect((180, v_pad), (180, 40)),
                                                                    "  ",
                                                                    manager=manager,
                                                                    object_id="config_window_label",
                                                                    container=self,
                                                                    parent_element=self,
                                                                    anchors={
                                                                        "left": "left",
                                                                        "top_target": self.numplayer_label
                                                                    })
            self.player_action_list.append(self.players_action)
            v_pad += 50

        # for i in range(len(self.player_action_list)):
        #     print(self.player_action_list[i])
        #     variable_name = "playerAction" + str(i)
        #     variable_value = self.player_action_list[i]
        #     exec(f"{variable_name} = {variable_value}")
        # print(playerAction0)