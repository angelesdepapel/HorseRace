import pygame

class Box:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
    
    def check_collision(self, other_rect):
        return self.rect.colliderect(other_rect)