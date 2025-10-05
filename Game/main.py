import pygame
import sys
import random
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DVD Screensaver")

# Colors
BLACK = (0, 0, 0)
COLORS = [
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 255, 0),  # Yellow
    (255, 0, 255),  # Magenta
    (0, 255, 255),  # Cyan
    (255, 165, 0),  # Orange
    (128, 0, 128)   # Purple
]

# Box properties
box_width, box_height = 100, 60
box_x = random.randint(0, WIDTH - box_width)
box_y = random.randint(0, HEIGHT - box_height)
box_speed_x = 3
box_speed_y = 3
box_color = random.choice(COLORS)

# Sound setup
#try:
    # Try to load a sound file (you'll need to provide your own sound file)
sound_path = os.path.join("resources", "sounds", "splat.wav")
bounce_sound = pygame.mixer.Sound(sound_path)
'''
except:
    # If no sound file is found, create a beep sound programmatically
    print("Sound file 'bounce.wav' not found. Using generated beep sound.")
    # Create a simple beep sound (440 Hz for 0.1 seconds)
    sample_rate = 44100
    duration = 100  # milliseconds
    frames = int(duration * sample_rate / 1000)
    arr = pygame.sndarray.array(pygame.Surface((frames, 1)))
    for i in range(frames):
        arr[i] = 32767 * 0.3 * (i * 440.0 / sample_rate * 2 * 3.14159)  # 440 Hz sine wave
    bounce_sound = pygame.mixer.Sound(buffer=arr)
'''
# Set volume
bounce_sound.set_volume(0.3)

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Move the box
    box_x += box_speed_x
    box_y += box_speed_y
    
    # Check for collisions with screen edges and play sound
    bounced = False
    if box_x <= 0 or box_x >= WIDTH - box_width:
        box_speed_x = -box_speed_x
        box_color = random.choice(COLORS)
        bounced = True
    
    if box_y <= 0 or box_y >= HEIGHT - box_height:
        box_speed_y = -box_speed_y
        box_color = random.choice(COLORS)
        bounced = True
    
    if bounced:
        bounce_sound.play()

    # Fill the screen with black
    screen.fill(BLACK)
    
    # Draw the box
    pygame.draw.rect(screen, box_color, (box_x, box_y, box_width, box_height))
    
    # Update the display
    pygame.display.flip()
    
    # Control the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()