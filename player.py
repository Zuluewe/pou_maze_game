import pygame

import view as View

player_position = pygame.Vector2(View.SCREENWIDTH() / 2, View.SCREENHEIGHT() / 2) # position in middle
player_sprite = pygame.image.load("assets/images/pou_hungry.png")
player_rect = player_sprite.get_rect

player_width = player_sprite.get_width()
player_height = player_sprite.get_height()


