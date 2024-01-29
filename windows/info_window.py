import pygame
import pygame_gui

class infoWindow(pygame_gui.elements.UIWindow):
    def __init__(self, manager, pos):
        super().__init__((pos),
                         manager,
                         window_display_title='How to Play Poker',
                         object_id='#info_window',
                         draggable=True)
        self.scroll_box = pygame_gui.elements.UIScrollingContainer(pygame.Rect((100, 200), (300, 200)),
                                                                                             manager=manager,
                                                                                             container=self
        )
        self.info_label = pygame_gui.elements.UILabel(pygame.Rect((50, 50), (200, 1)),
                                                      "",
                                                      manager=manager,
                                                      container=self.scroll_box
        )
    def load_text(self, file_path):
        try:
            with open(file_path, 'r') as file:
                text = file.read()
                self.info_label.set_text(text)
                self.scroll_box.set_dimensions((400, 400))
        except FileNotFoundError:
            print(f"File not found: {file_path}")