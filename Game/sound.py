import pygame
import os

class SoundManager:
    def __init__(self):
        self.sounds = {}
        
    def load_sound(self, name, filepath):
        """Load a sound file and store it with a name"""
        try:
            sound = pygame.mixer.Sound(filepath)
            self.sounds[name] = sound
            return True
        except pygame.error as e:
            print(f"Error loading sound {filepath}: {e}")
            return False
    
    def play_sound(self, name, volume=0.5):
        """Play a loaded sound by name"""
        if name in self.sounds:
            self.sounds[name].set_volume(volume)
            self.sounds[name].play()
    
    def set_volume(self, name, volume):
        """Set volume for a specific sound"""
        if name in self.sounds:
            self.sounds[name].set_volume(volume)