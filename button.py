import pygame

class Button:
    def __init__(self, x, y, width, height, text, color_normal, color_hover, font, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color_normal = color_normal
        self.color_hover = color_hover
        self.font = font
        self.text_color = text_color
        self.is_hover = False
        
    def draw(self, screen):
        if self.is_hovered:
            pygame.draw.rect(screen, self.color_hover, self.rect)
        else:
            pygame.draw.rect(screen, self.color_normal, self.rect)
        
        font_surface = self.font.render(self.text, True, self.text_color)
        font_rect = font_surface.get_rect(center = self.rect.center)
        screen.blit(font_surface, font_rect)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
    def is_clicked(self, pos):
        if self.rect.collidepoint(*pos):
            return True
        return False