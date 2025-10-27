import pygame
import sys
from Horse import Horse
from sound import SoundManager
from map import Map
from premio import Carrot
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
azul = Horse(WIDTH, HEIGHT, start_pos=(113, 40), image="azul.png", name="azul")
amarillo = Horse(WIDTH, HEIGHT, start_pos=(196, 40), image="amarillo.png", name="amarillo")
cafe = Horse(WIDTH, HEIGHT, start_pos=(100, 100), image="cafe.png", name="cafe")
blanco = Horse(WIDTH, HEIGHT, start_pos=(179, 100), image="blanco.png", name="blanco")
naranjo = Horse(WIDTH, HEIGHT, start_pos=(239, 100), image="naranjo.png", name="naranjo")
cyan = Horse(WIDTH, HEIGHT, start_pos=(113, 160), image="cyan.png", name="cyan")
gris = Horse(WIDTH, HEIGHT, start_pos=(196, 160), image="gris.png", name="gris")
horses = [azul,
          amarillo,
          cafe,
          blanco,
          naranjo,
          cyan,
          gris,]

for horse in horses:
    for rival in horses:
        if horse != rival:
            horse.rivals.append(rival)

# Create Map
game_map = Map(WIDTH, HEIGHT)
# Create multiple stationary boxes
boxes = game_map.box_list()

#premio
carrot = Carrot(WIDTH, HEIGHT)

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
    for horse in horses:
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
    for horse in horses:
        horse.draw(screen)
        if horse._winner(carrot):
            print(horse.name, "es el ganador :)")
            running = False

    carrot.draw(screen)
    
    # Update the display
    pygame.display.flip()
    
    # Control the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()