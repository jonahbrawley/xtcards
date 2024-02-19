import pygame
import pygame_gui
# from windows.log_window import logWindow

class bankWindow(pygame_gui.elements.UIWindow):
    def __init__(self, manager, pos):
        super().__init__((pos),
                        manager,
                        window_display_title='The Holy Bank',
                        object_id='#setup_window',
                        draggable=False)
        
        self.show_log = False

        self.bank_label = pygame_gui.elements.UILabel(pygame.Rect((0, 20), (180, 40)),
                                                                    "Value:",
                                                                    manager=manager,
                                                                    object_id="header_game",
                                                                    container=self,
                                                                    parent_element=self,
                                                                    anchors={
                                                                        "top": "top",
                                                                        "centerx": "centerx"
                                                                    })
        self.value_label = pygame_gui.elements.UILabel(pygame.Rect((0, 20), (180, 40)),
                                                                    "0",
                                                                    manager=manager,
                                                                    object_id="header_game",
                                                                    container=self,
                                                                    parent_element=self,
                                                                    anchors={
                                                                        "top_target": self.bank_label,
                                                                        "centerx": "centerx"
                                                                    })
        self.log_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, -60), ((100), 40)),
                                                            text='Log',
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
            if (event.ui_element == self.log_button):
                self.show_log = True
                print('PLAY: Drawing log window')
