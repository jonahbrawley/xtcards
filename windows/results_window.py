import pygame
import pygame_gui

class resultsWindow(pygame_gui.elements.UIWindow):
    def __init__(self, manager, pos):
        super().__init__((pos),
                        manager,
                        window_display_title='Righteous Winning Hand (Holy Hand)',
                        object_id='#setup_window',
                        draggable=False)
        
        card_width = pos.width*.16
        card_height = card_width * 1.4

        padding = pos.width*.02 # padding inbetween cards
        cardinc = padding
        
        imgsurf = pygame.Surface(size=(card_width, card_height))
        imgsurf.fill((40, 62, 51))
        
        self.card1 = pygame_gui.elements.UIImage(pygame.Rect((cardinc, pos.height*.2), (card_width, card_height)),
                                                          image_surface=imgsurf,
                                                          manager=manager,
                                                          container=self,
                                                          parent_element=self
        )
        cardinc = cardinc + card_width + padding
        self.card2 = pygame_gui.elements.UIImage(pygame.Rect((cardinc, pos.height*.2), (card_width, card_height)),
                                                          image_surface=imgsurf,
                                                          manager=manager,
                                                          container=self,
                                                          parent_element=self
        )
        cardinc = cardinc + card_width + padding
        self.card3 = pygame_gui.elements.UIImage(pygame.Rect((cardinc, pos.height*.2), (card_width, card_height)),
                                                          image_surface=imgsurf,
                                                          manager=manager,
                                                          container=self,
                                                          parent_element=self
        )
        cardinc = cardinc + card_width + padding
        self.card4 = pygame_gui.elements.UIImage(pygame.Rect((cardinc, pos.height*.2), (card_width, card_height)),
                                                          image_surface=imgsurf,
                                                          manager=manager,
                                                          container=self,
                                                          parent_element=self
        )
        cardinc = cardinc + card_width + padding
        self.card5 = pygame_gui.elements.UIImage(pygame.Rect((cardinc, pos.height*.2), (card_width, card_height)),
                                                          image_surface=imgsurf,
                                                          manager=manager,
                                                          container=self,
                                                          parent_element=self
        )