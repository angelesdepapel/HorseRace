import pygame
import sys
from Horse import Horse
from sound import SoundManager
from map import Map
import random

seed = input("semilla: ")
seed = int(seed)
random.seed(seed)

# Initialize Pygame
pygame.init()

# Set up fullscreen display
screen = pygame.display.set_mode((1080, 720))
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Carrera de Caballos")

# Colors
BACKGROUND_COLOR = (0, 204, 102)  # Green color

# Initialize sound manager and load sounds
sound_manager = SoundManager()
sound_manager.load_sound("clop", "resources/sounds/clop.wav")

# Create horse
horse = Horse(WIDTH, HEIGHT)

# Create Map
game_map = Map(WIDTH, HEIGHT)
# Create multiple stationary boxes

boxes = game_map.box_list()

box_actual = boxes[0]

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_DOWN:
                box_actual.move(0, 10)
            elif event.key == pygame.K_UP:
                box_actual.move(0, -10)
            elif event.key == pygame.K_LEFT:
                box_actual.move(-10, 0)
            elif event.key == pygame.K_RIGHT:
                box_actual.move(10, 0)
            
            elif event.key == pygame.K_w:
                box_actual.scale(0, -10)
            elif event.key == pygame.K_s:
                box_actual.scale(0, 10)
            elif event.key == pygame.K_a:
                box_actual.scale(-10, 0)
            elif event.key == pygame.K_d:
                box_actual.scale(10, 0)
            
            elif event.key == pygame.K_SPACE:
                box_actual.print()
        
    
    # Update horse
    bounced = horse.update(boxes)
    
    # Play sound if horse bounced
    if bounced:
        sound_manager.play_sound("clop", volume=0.3)
    
    # Fill the screen with green background
    screen.fill(BACKGROUND_COLOR)
    
    # Draw all boxes
    for box in boxes:
        box.draw(screen)
    
    # Draw horse
    horse.draw(screen)
    
    # Update the display
    pygame.display.flip()
    
    # Control the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()