import pygame
import pygame_gui

class tableWindow(pygame_gui.elements.UIWindow):
    def __init__(self, manager, pos):
        super().__init__((pos),
                        manager,
                        window_display_title='The Table',
                        object_id='#setup_window',
                        draggable=False)
        
        self.card1 = None
        self.card2 = None
        self.card3 = None
        self.card4 = None
        self.card5 = None

        card_width = pos.width*.16
        card_height = card_width * 1.4

        imgsurf = pygame.Surface(size=(card_width, card_height))
        # imgsurf.fill((0, 0, 0)) # black color for debug

        self.table_cards = [self.card1, self.card2, self.card3, self.card4, self.card5]
        padding = pos.width*.02 # padding inbetween cards
        cardinc = padding  

        for card in self.table_cards:
            card = pygame_gui.elements.UIImage(pygame.Rect((cardinc, pos.height*.2), (card_width, card_height)),
                                                            image_surface=imgsurf,
                                                            manager=manager,
                                                            container=self,
                                                            parent_element=self
                                                            )
            cardinc = cardinc + card_width + padding