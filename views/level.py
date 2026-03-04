# view

import pygame
from maze_generator import Maze
SCREENWIDTH = 1060
SCREENHEIGHT = 720
FPS = 60

pygame.init()
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("Level")
clock = pygame.time.Clock()

class Level:
    def __init__(self, screen, font, gameStateManager, player_sprite):
        self.display = screen
        self.font = font
        self.gameState = gameStateManager
        self.player_sprite = player_sprite

    def draw(self, model):
        self.display.fill("#50b032") # pou grass green
        self.display.blit(self.player_sprite, model.player_position)

        # define text
        score_text = self.font.render(f"Score: {model.score}", True, "white")

        # render text
        self.display.blit(score_text, (10, 10))

        #render maze
        maze = Maze()
        maze.screen = self.display
        maze.draw_grid()
        maze.generate(0,0)

running = True
while running:
    # process input (events)
    for event in pygame.event.get():
        # check for closing the window
        if event.type == pygame.QUIT:
            running = False
    clock.tick(60)
pygame.quit()


"""class Level:
    def __init__(self, display, gameStateManager, font):
        self.display = display
        self.gameState = gameStateManager
        self.font = font

    def run(self):
        self.display.fill("#50b032") # grass green

    # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            key_press = pygame.key.get_pressed()
            if key_press[pygame.K_ESCAPE]:
                self.gameState.set_states("Pause")
"""