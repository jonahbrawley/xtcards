import pygame
import pygame_gui

class logWindow(pygame_gui.elements.UIWindow):
    def __init__ (self, manager, pos):
        super().__init__((pos),
                         manager,
                         window_display_title='The Holy Log',
                         object_id='#setup_window',
                         draggable=True)
        
        self.game_log = pygame_gui.elements.UITextBox("Sample text here",
                                                      relative_rect=pygame.Rect((0.000001 * pos.width, 0.02 * pos.height), (0.875 * pos.width, 0.825 * pos.height)),
                                                            manager=manager,
                                                            container=self,
                                                            parent_element=self,
                                                            anchors={
                                                            "centerx": "centerx"})