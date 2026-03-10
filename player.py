# model

import pygame
import food as food
import screenvariable

class Player:
    def __init__(self, position, sprite):
        self.position = position
        self.sprite = sprite
        self.rect = self.sprite.get_rect(topleft=self.position)

    def draw(self, screen):
        screen.blit(self.sprite, self.rect)

    def check_collision(self, food): # collision with food
        self.sprite = pygame.image.load("assets/images/pou_happy.png") # change from hungry to happy


"""player_position = pygame.Vector2(screenvariable.SCREENWIDTH() / 2, screenvariable.SCREENHEIGHT() / 2) # position in middle
player_sprite = pygame.image.load("assets/images/pou_hungry.png")
player_rect = player_sprite.get_rect

player_width = player_sprite.get_width()
player_height = player_sprite.get_height()"""


