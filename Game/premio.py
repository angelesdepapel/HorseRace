import pygame
import os

class Carrot:
    def __init__(self, screen_width, screen_height, start_pos=(930, 160), image="carrot.png"):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # load carrot image
        image_path = os.path.join("resources", "images", image)
        original_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(original_image, (30, 30))
        self.image = self.image.convert_alpha()

        # Set up rectangle
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = start_pos
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)