# view

import pygame
import controller as CON

import models.maze_generator as MAZE

pygame.init()
screen = pygame.display.set_mode((CON.SCREENWIDTH, CON.SCREENHEIGHTHEIGHT))
pygame.display.set_caption("Level")
clock = pygame.time.Clock()

class Level:
    def __init__(self, display, font, gameStateManager, player_sprite):
        self.display = display
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
        MAZE.maze = MAZE.Maze()
        MAZE.maze.draw_grid()
        MAZE.maze.generate(0,0)

running = True
while running:
    # process input (events)
    for event in pygame.event.get():
        # check for closing the window
        if event.type == pygame.QUIT:
            running = False
    pygame.display.set_caption(f"Levels visited: {len(MAZE.maze.visited)})")
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