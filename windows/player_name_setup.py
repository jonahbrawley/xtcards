import pygame
import pygame_gui

class playerNameSetupWindow(pygame_gui.elements.UIWindow):
    submitPlayerClicked = False
    ai_player_count = 1
    playerNames = []

    def __init__(self, manager, pos, playercount):
        self.playercount = playercount
        self.playernames = []

        super().__init__((pos),
                        manager,
                        window_display_title='Player Names',
                        object_id='#setup_window',
                        draggable=False)
        v_pad = 30
        h_pad = 30

        self.player_name = []
        self.player_name_labels = []
        for i in range(self.playercount):
            player_name_label = pygame_gui.elements.UITextEntryLine(
            pygame.Rect((h_pad, v_pad), (200, 40)),
            placeholder_text=f"player{i+1}",  # Use f-string to include the player number in the initial text
            container=self,
            parent_element=self,
            anchors={"left": "left"}
            )
            player_name_label.set_text_length_limit(9),
            self.player_name_labels.append(player_name_label)  # Add the label to the list
            v_pad += 50
        self.submit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, -60), ((160), 40)),
                                                            text='Submit',
                                                            manager=manager,
                                                            container=self,
                                                            parent_element=self,
                                                            anchors={
                                                                "bottom": "bottom",
                                                                "centerx": "centerx"
                                                            })
            
    def process_event(self, event):

        handled = super().process_event(event)

        if (event.type == pygame_gui.UI_BUTTON_PRESSED):
            if (event.ui_element == self.submit_button):
                i = 1
                self.player_name = [label.get_text() for label in self.player_name_labels]
                
                # TODO: FIX POSSIBILITIES OF EMPTY NAMES ('')

                self.playerNames = self.player_name
                playerNameSetupWindow.submitPlayerClicked = True
                self.kill()
                print(self.playerNames)
        self.playerNames = self.player_name