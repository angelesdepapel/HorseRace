import pygame
import sys
from Horse import Horse
from sound import SoundManager
from box import Box

# Initialize Pygame
pygame.init()

# Set up fullscreen display
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Bouncing Horse")

# Colors
BACKGROUND_COLOR = (0, 204, 102)  # Green color

# Initialize sound manager and load sounds
sound_manager = SoundManager()
sound_manager.load_sound("clop", "resources/sounds/clop.wav")

# Create horse
horse = Horse(WIDTH, HEIGHT)

# Create multiple stationary boxes
boxes = [
    Box(WIDTH//2 - 50, HEIGHT//2 - 50, 100, 100, (255, 0, 0)),    # Center
    Box(100, 100, 80, 80, (0, 0, 255)),                           # Top-left
    Box(WIDTH - 180, 100, 80, 80, (0, 0, 255)),                   # Top-right
    Box(100, HEIGHT - 180, 80, 80, (0, 0, 255)),                  # Bottom-left
    Box(WIDTH - 180, HEIGHT - 180, 80, 80, (0, 0, 255)),          # Bottom-right
    Box(WIDTH//4, HEIGHT//3, 60, 60, (255, 255, 0)),              # Random position
    Box(WIDTH*3//4, HEIGHT*2//3, 60, 60, (255, 255, 0))           # Random position
]

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