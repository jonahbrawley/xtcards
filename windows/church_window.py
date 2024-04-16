import pygame
import pygame_gui
import webbrowser

class churchWindow(pygame_gui.elements.UIWindow):
    def __init__(self, manager, pos):
        super().__init__((pos),
                         manager,
                         window_display_title='How to Donate!',
                         object_id='#church_window',
                         draggable=True)
        self.donation_label = pygame_gui.elements.UITextBox("Please click the button below to donate in support for our local church. We hope you enjoyed using xtcards, God bless you! :)",
                                                            relative_rect=pygame.Rect((0.000001 * pos.width, 0.05 * pos.height), (0.75 * pos.width, 0.5 * pos.height)),
                                                            manager=manager,
                                                            container=self,
                                                            parent_element=self,
                                                            anchors={
                                                            "centerx": "centerx"
                                                            })
        self.donate_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0.27 * pos.width, 0.7 * pos.height), (0.38 * pos.width, 0.12 * pos.height)),
                                                          text='Donate',
                                                          manager=manager,
                                                          container=self,
                                                          parent_element=self,
                                                          anchors={
                                                              "bottom': 'bottom",
                                                              "centerx': 'centerx"
                                                          })
    def process_event(self, event):
        super().process_event(event)
        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.donate_button:
                webbrowser.open("https://magonline.com/give/")