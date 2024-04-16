import pygame
import pygame_gui

from random import shuffle

# Used to display player information during the game

class playerWindow(pygame_gui.elements.UIWindow):
    aiPlayerNames = ["HolyBot", "AngelAI", "GodBot", "NoahsAI"]
    shuffle(aiPlayerNames)
    def __init__(self, manager, pos, playernames, chipcount, aiplayercount, init):
        super().__init__((pos),
                         manager,
                         window_display_title='Players',
                         object_id='#setup_window',
                         draggable=False)

        if (init):
            self.playernames = playernames
            self.chipcount = chipcount
            self.aiplayercount = aiplayercount

            self.players_label = None

            v_pad = 10

            windowSpacer = pos.height * .05
            infoRect = pygame.Rect((20, windowSpacer), (pos.width, 40))

            self.numplayer_label = pygame_gui.elements.UILabel(infoRect,
                                                                        "  player: chips | action",
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
                self.players_action = pygame_gui.elements.UILabel(pygame.Rect((200, v_pad), (180, 40)),
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
                self.player_labels_list.append(self.ai_players_label)
                self.players_action = pygame_gui.elements.UILabel(pygame.Rect((200, v_pad), (180, 40)),
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

    def load(self, manager, pos, players, chip_counts): # used to reload player window after saving
        self.players_label = None

        v_pad = 10

        windowSpacer = pos.height * .05
        infoRect = pygame.Rect((20, windowSpacer), (pos.width, 40))

        self.numplayer_label = pygame_gui.elements.UILabel(infoRect,
                                                           "  player: chips | action",
                                                           manager=manager,
                                                           object_id="config_window_label",
                                                           container=self,
                                                           parent_element=self,
                                                           anchors={
                                                               "centerx": "centerx"
                                                           })
        self.player_labels_list = []
        self.player_action_list = []
        for i in range(len(players)):
            self.players_label = pygame_gui.elements.UILabel(pygame.Rect((20, v_pad), (180, 40)),
                                                             players[i].name + ":  " + str(
                                                                 chip_counts[i]) + "  |  ",
                                                             manager=manager,
                                                             object_id="config_window_label",
                                                             container=self,
                                                             parent_element=self,
                                                             anchors={
                                                                 "left": "left",
                                                                 "top_target": self.numplayer_label
                                                             })
            self.player_labels_list.append(self.players_label)
            self.players_action = pygame_gui.elements.UILabel(pygame.Rect((200, v_pad), (180, 40)),
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
        # for i in range(self.aiplayercount):
        #     self.ai_players_label = pygame_gui.elements.UILabel(pygame.Rect((20, v_pad), (180, 40)),
        #                                                         playerWindow.aiPlayerNames[i] + ":  " + str(
        #                                                             self.chipcount) + "  |  ",
        #                                                         manager=manager,
        #                                                         object_id="config_window_label",
        #                                                         container=self,
        #                                                         parent_element=self,
        #                                                         anchors={
        #                                                             "left": "left",
        #                                                             "top_target": self.numplayer_label
        #                                                         })
        #     self.player_labels_list.append(self.ai_players_label)
        #     self.players_action = pygame_gui.elements.UILabel(pygame.Rect((200, v_pad), (180, 40)),
        #                                                       "  ",
        #                                                       manager=manager,
        #                                                       object_id="config_window_label",
        #                                                       container=self,
        #                                                       parent_element=self,
        #                                                       anchors={
        #                                                           "left": "left",
        #                                                           "top_target": self.numplayer_label
        #                                                       })
        #     self.player_action_list.append(self.players_action)
        #     v_pad += 50


        # for i in range(len(self.player_action_list)):
        #     print(self.player_action_list[i])
        #     variable_name = "playerAction" + str(i)
        #     variable_value = self.player_action_list[i]
        #     exec(f"{variable_name} = {variable_value}")
        # print(playerAction0)