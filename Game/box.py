import pygame

class Box:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
    
    def check_collision(self, other_rect):
        return self.rect.colliderect(other_rect)
    
    def move(self, x, y):
        self.rect.update(self.rect.x + x,
                         self.rect.y + y,
                         self.rect.width,
                         self.rect.height)

    def scale(self, width, height):
        self.rect.update(self.rect.x,
                         self.rect.y,
                         self.rect.width + width,
                         self.rect.height + height)
    
    def print(self):
        print(self.rect.x, 
              self.rect.y, 
              self.rect.width, 
              self.rect.height)