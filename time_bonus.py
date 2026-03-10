# model

import pygame
from object import GameObject

class TimeBonus(GameObject):
    def __init__(self, position, sprite, timer, sound=None):
        super().__init__(position, sprite)
        self.timer = timer
        self.sound = pygame.mixer.Sound("assets/sounds/timer.ogg") # identify food eating sound

    def on_collision(self):
        self.timer += 5 # add 5 second to time
        self.sound.play()
        return super().on_collision()