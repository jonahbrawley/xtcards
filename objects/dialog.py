import pygame

class Dialog:
    def draw(self, window: pygame.Surface):
        # draws itself on provided surface window
        pass
        
    def is_hovered(self, pos):
        # determines if window is hovered by cursor
        pass

    def move(self, rel):
        # moves to position relative to cursor
        # self.rect.move_ip(rel)
        pass
