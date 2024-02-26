import pygame
import pygame_gui

class tableWindow(pygame_gui.elements.UIWindow):
    def __init__(self, manager, pos):
        super().__init__((pos),
                        manager,
                        window_display_title='The Table',
                        object_id='#setup_window',
                        draggable=False)
        
        card_width = pos.width*.16
        card_height = card_width*1.4

        padding = (pos.width - (card_width * 5)) / 10

        card3x = 0
        card2x = card3x - card_width - padding
        card1x = card2x - card_width - padding
        card4x = card3x + card_width + padding
        card5x = card4x + card_width + padding

        imgsurf = pygame.Surface(size=(card_width, card_height))
        imgsurf.fill((40, 62, 51))

        self.card1 = pygame_gui.elements.UIImage(pygame.Rect((card1x, pos.height*.2), (card_width, card_height)),
                                                          image_surface=imgsurf,
                                                          manager=manager,
                                                          container=self,
                                                          parent_element=self,
                                                          anchors = {
                                                             "centerx": "centerx"
                                                          }
        )
        self.card2 = pygame_gui.elements.UIImage(pygame.Rect((card2x, pos.height*.2), (card_width, card_height)),
                                                          image_surface=imgsurf,
                                                          manager=manager,
                                                          container=self,
                                                          parent_element=self,
                                                        anchors={
                                                             "centerx": "centerx"
                                                        }
        )
        self.card3 = pygame_gui.elements.UIImage(pygame.Rect((card3x, pos.height*.2), (card_width, card_height)),
                                                          image_surface=imgsurf,
                                                          manager=manager,
                                                          container=self,
                                                          parent_element=self,
                                                          anchors={
                                                             "centerx": "centerx"
                                                          }
        )
        self.card4 = pygame_gui.elements.UIImage(pygame.Rect((card4x, pos.height*.2), (card_width, card_height)),
                                                          image_surface=imgsurf,
                                                          manager=manager,
                                                          container=self,
                                                          parent_element=self,
                                                 anchors={
                                                     "centerx": "centerx"
                                                 }
        )
        self.card5 = pygame_gui.elements.UIImage(pygame.Rect((card5x, pos.height*.2), (card_width, card_height)),
                                                          image_surface=imgsurf,
                                                          manager=manager,
                                                          container=self,
                                                          parent_element=self,
                                                 anchors={
                                                     "centerx": "centerx"
                                                 }
        )