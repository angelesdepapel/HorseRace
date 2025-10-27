import pygame
import random
import math
import os

class Horse:
    def __init__(self, screen_width, screen_height, start_pos=(100, 100), name="DEFAULT HORSE"):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Load horse image and scale to 50x50
        image_path = os.path.join("resources", "images", "horse.png")
        original_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(original_image, (50, 50))
        self.image = self.image.convert_alpha()
        
        # Set up rectangle
        self.rect = self.image.get_rect()
        
        # rival horses
        self.rivals : list[Horse] = []

        # starting pos
        x, y = start_pos
        self.rect.x = x-25
        self.rect.y = y
        # Random initial angle
        self.speed = 5
        angle = random.uniform(0, 2 * math.pi)
        self.speed_x = self.speed * math.cos(angle)
        self.speed_y = self.speed * math.sin(angle)
    
    def update(self, boxes):
        # Store old position for collision resolution
        old_x, old_y = self.rect.x, self.rect.y
        
        # Move the horse
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        # Check for box collisions
        box_bounce = self._check_box_collisions(boxes, old_x, old_y)
        horse_bounce = self._check_horse_collisions(old_x, old_y)
        
        return box_bounce or horse_bounce
    
    def _check_horse_collisions(self, old_x, old_y):
        for rival in self.rivals:
            if self.rect.colliderect(rival.rect):
                self._handle_box_collision(rival.rect, old_x, old_y)
                return True
        return False
        
    
    def _check_box_collisions(self, boxes, old_x, old_y):
        for box in boxes:
            if box.check_collision(self.rect):
                self._handle_box_collision(box.rect, old_x, old_y)
                return True
        return False
    
    def _handle_box_collision(self, box_rect: pygame.Rect, old_x, old_y):
        # Calculate collision side
        dx = (self.rect.centerx - box_rect.centerx) / (box_rect.width / 2)
        dy = (self.rect.centery - box_rect.centery) / (box_rect.height / 2)
        
        # Determine which side was hit based on the larger overlap
        overlap_left = self.rect.right - box_rect.left
        overlap_right = box_rect.right - self.rect.left
        overlap_top = self.rect.bottom - box_rect.top
        overlap_bottom = box_rect.bottom - self.rect.top
        
        # Find the smallest overlap to determine collision side
        min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)
        
        # Restore old position
        self.rect.x = old_x
        self.rect.y = old_y
        
        # Apply realistic bounce based on collision side
        if min_overlap == overlap_left or min_overlap == overlap_right:  
            self.speed_x = -self.speed_x  # Bounce r
        else:
            self.speed_y = -self.speed_y
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)