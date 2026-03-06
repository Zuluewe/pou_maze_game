# model

import pygame
import views.variable as variable

class Player:


player_position = pygame.Vector2(variable.SCREENWIDTH() / 2, variable.SCREENHEIGHT() / 2) # position in middle
player_sprite = pygame.image.load("assets/images/pou_hungry.png")
player_rect = player_sprite.get_rect

player_width = player_sprite.get_width()
player_height = player_sprite.get_height()


