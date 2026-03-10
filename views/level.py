# view

import pygame
<<<<<<< HEAD
from maze_generator import Maze
SCREENWIDTH = 1060
SCREENHEIGHT = 720
FPS = 60

CELL_SIZE = 50
GRID_SIZE = 5
OFFSET_X = 50
OFFSET_Y = 50
MAZE_WIDTH = GRID_SIZE * CELL_SIZE


pygame.init()
pygame.display.set_caption("Level")
clock = pygame.time.Clock()
=======

import variable
import models.player as player
from maze_generator import Maze
>>>>>>> 677c244e8d6e0d0bcce81ccaa0034d3756e6b026

class Level:
    def __init__(self, screen, font, gameStateManager, player_sprite):
        self.display = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        self.font = font
        self.gameState = gameStateManager
        self.player_sprite = player_sprite
        
        # create a maze instance once and reuse it
        self.maze = Maze(self.display)
<<<<<<< HEAD
        self.maze.generate(0,0)
        self.maze_surface = pygame.Surface((SCREENWIDTH, SCREENHEIGHT))
        self.maze_surface.fill("#50b032")
        self.maze.draw_grid(screen=self.maze_surface)
        
        #(r,c) coordinates for the player position
        self.player_row = 0
        self.player_col = 0
        half = self.maze.cell_size // 2
        self.player_position = (
            self.maze.offset_x + self.player_col * self.maze.cell_size + half - self.player_sprite.get_width() // 2,
            self.maze.offset_y + self.player_row * self.maze.cell_size + half - self.player_sprite.get_height() // 2
        )
    def draw(self):
        '''self.display.fill("#50b032") # pou grass green
        self.maze.draw_grid() # draw the maze grid'''
        self.display.blit(self.player_sprite, self.player_position)
=======

    def draw(self, model):
        self.display.fill("#50b032") # pou grass green
        self.display.blit(player.sprite, player.position)
>>>>>>> 677c244e8d6e0d0bcce81ccaa0034d3756e6b026

        # define text
        score_text = self.font.render(f"Score: , True, ")

        # render text
        self.display.blit(score_text, (10, 10))
        pygame.display.flip() # update the display after drawing everything
        
    def update(self):
        keys = pygame.key.get_pressed()
        maze_connections = self.maze.grid_connections
        dx, dy = 0, 0

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if 'right' in maze_connections[(self.player_row, self.player_col)]:
                dx = 1
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if 'left' in maze_connections[(self.player_row, self.player_col)]:
                dx = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if 'down' in maze_connections[(self.player_row, self.player_col)]:
                dy = 1
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            if 'up' in maze_connections[(self.player_row, self.player_col)]:
                dy = -1
        
        if dx != 0 or dy != 0:
            new_r = self.player_row + dy
            new_c = self.player_col + dx

            # safety (should not be needed if connections are correct)
            if 0 <= new_r < self.maze.grid_size and 0 <= new_c < self.maze.grid_size:
                self.player_row = new_r
                self.player_col = new_c

                # Update pixel position
                half = self.maze.cell_size // 2
                self.player_position = (
                    self.maze.offset_x + new_c * self.maze.cell_size + half - self.player_sprite.get_width() // 2,
                    self.maze.offset_y + new_r * self.maze.cell_size + half - self.player_sprite.get_height() // 2
                )

if __name__ == "__main__":
<<<<<<< HEAD
    # Dummy objects for testing
    dummy_font = pygame.font.SysFont(None, 36)
    dummy_sprite = pygame.Surface((40, 40))
    dummy_sprite.fill((255, 100, 100))          # red square as player
=======
    pygame.init()
    screen = pygame.display.set_mode((variable.SCREENWIDTH, variable.SCREENHEIGHT))
    pygame.display.set_caption("Pou Maze Game")
    clock = pygame.time.Clock()
>>>>>>> 677c244e8d6e0d0bcce81ccaa0034d3756e6b026

    level = Level(screen, dummy_font, None, dummy_sprite)
    running = True
          
    while running:
<<<<<<< HEAD
        
=======
        maze = Maze(screen)
        maze.draw_grid()
        maze.generate(0, 0)
>>>>>>> 677c244e8d6e0d0bcce81ccaa0034d3756e6b026
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