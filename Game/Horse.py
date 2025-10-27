import pygame
import random
import math
import os

class Horse:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Load horse image and scale to 50x50
        image_path = os.path.join("resources", "images", "horse.png")
        original_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(original_image, (50, 50))
        self.image = self.image.convert_alpha()
        
        # Set up rectangle
        self.rect = self.image.get_rect()
        
        # Random starting position
        self.rect.x = random.randint(0, screen_width - 50)
        self.rect.y = random.randint(0, screen_height - 50)
        
        # Random initial velocity
        self.speed = random.uniform(3.0, 6.0)
        angle = random.uniform(0, 2 * math.pi)
        self.speed_x = self.speed * math.cos(angle)
        self.speed_y = self.speed * math.sin(angle)
    
    def update(self, boxes):
        # Store old position for collision resolution
        old_x, old_y = self.rect.x, self.rect.y
        
        # Move the horse
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        # Check for wall collisions
        wall_bounce = self._check_wall_collision()
        
        # Check for box collisions
        box_bounce = self._check_box_collisions(boxes, old_x, old_y)
        
        return wall_bounce or box_bounce
    
    def _check_wall_collision(self):
        bounced = False
        
        # Left wall
        if self.rect.left <= 0:
            self.rect.left = 0
            self.speed_x = abs(self.speed_x)
            bounced = True
        
        # Right wall
        elif self.rect.right >= self.screen_width:
            self.rect.right = self.screen_width
            self.speed_x = -abs(self.speed_x)
            bounced = True
        
        # Top wall
        if self.rect.top <= 0:
            self.rect.top = 0
            self.speed_y = abs(self.speed_y)
            bounced = True
        
        # Bottom wall
        elif self.rect.bottom >= self.screen_height:
            self.rect.bottom = self.screen_height
            self.speed_y = -abs(self.speed_y)
            bounced = True
        
        return bounced
    
    def _check_box_collisions(self, boxes, old_x, old_y):
        bounced = False
        for box in boxes:
            if box.check_collision(self.rect):
                self._handle_box_collision(box.rect, old_x, old_y)
                bounced = True
                break  # Only handle one collision per frame
        return bounced
    
    def _handle_box_collision(self, box_rect, old_x, old_y):
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
        if min_overlap == overlap_left:  # Left side of box
            self.speed_x = abs(self.speed_x)  # Bounce right
        elif min_overlap == overlap_right:  # Right side of box
            self.speed_x = -abs(self.speed_x)  # Bounce left
        elif min_overlap == overlap_top:  # Top of box
            self.speed_y = abs(self.speed_y)  # Bounce down
        elif min_overlap == overlap_bottom:  # Bottom of box
            self.speed_y = -abs(self.speed_y)  # Bounce up
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)