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
                                                            relative_rect=pygame.Rect((0, 10), (pos.width/1.5, pos.height/2)),
                                                            manager=manager,
                                                            container=self,
                                                            parent_element=self,
                                                            anchors={
                                                            "centerx": "centerx"
                                                            })
        self.donate_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((125, 300), (pos.width/3.8, pos.height/8.5)),
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