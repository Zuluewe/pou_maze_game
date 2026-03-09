# view

import pygame

import variable
import models.player as player
from maze_generator import Maze


class Level:
    def __init__(self, screen, font, gameStateManager, player_sprite):
        self.display = screen
        self.font = font
        self.gameState = gameStateManager
        self.player_sprite = player_sprite
        
        # create a maze instance once and reuse it
        self.maze = Maze(self.display)

    def draw(self, model):
        self.display.fill("#50b032") # pou grass green
        self.display.blit(player.sprite, player.position)

        # define text
        score_text = self.font.render(f"Score: {model.score}", True, "white")

        # render text
        self.display.blit(score_text, (10, 10))

        

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((variable.SCREENWIDTH, variable.SCREENHEIGHT))
    pygame.display.set_caption("Pou Maze Game")
    clock = pygame.time.Clock()

    running = True
    while running:
        maze = Maze(screen)
        maze.draw_grid()
        maze.generate(0, 0)
        for event in pygame.event.get():
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