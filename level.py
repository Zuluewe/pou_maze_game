# view

import pygame
#from maze_generator import Maze
#from views.maze_generator import Maze
import maze_generator
SCREENWIDTH = 1060
SCREENHEIGHT = 720
FPS = 60

CELL_SIZE = 50
GRID_SIZE = 5
OFFSET_X = 150
OFFSET_Y = 150
MAZE_WIDTH = GRID_SIZE * CELL_SIZE


pygame.init()
display = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
display.fill("#50b032") # grass green
pygame.display.set_caption("Level")
font = pygame.font.Font("assets/PouFont.ttf", 32)
clock = pygame.time.Clock()

class Level:
    def __init__(self, display, gameStateManager, font, player_sprite):
        self.display = display
        self.font = font
        self.gameState = gameStateManager
        self.player_sprite = player_sprite
    #(r,c) coordinates for the player position
        self.player_row = 0
        self.player_col = 0
    # generate the maze once during initialization
        self.maze = maze_generator.Maze(self.display, GRID_SIZE, CELL_SIZE, OFFSET_X, OFFSET_Y,("#3f5837"))
        self.maze.generate(0,0) 

    #player start
        half = self.maze.cell_size // 2
        self.player_position = (
            self.maze.offset_x + self.player_col * self.maze.cell_size + half - self.player_sprite.get_width() // 2,
            self.maze.offset_y + self.player_row * self.maze.cell_size + half - self.player_sprite.get_height() // 2
        
        ) # 50 + (0 * 50) + 25 - half of the player sprite = 75, same for y. This centers the player sprite in the cell 

        
        self.draw() # draw the initial state of the level      

    def draw(self):      
        
        self.display.blit(self.player_sprite, self.player_position)
        # define text
        score_text = font.render(f"Score: 0", True, "white")
        # render text
        self.display.blit(score_text, (10, 10))
        pygame.display.flip() # update the display after drawing everything
        
    def update(self):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        current_cell = (self.player_row, self.player_col)
        connections = self.maze.grid_connections.get(current_cell, set())


        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if 'right' in connections:
                dx = 1
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if 'left' in connections:
                dx = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if 'down' in connections:
                dy = 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if 'up' in connections:
                dy = -1
        
        if dx != 0 or dy != 0:
            new_r = self.player_row + dy
            new_c = self.player_col + dx

            # should not be needed if connections are correct
            if 0 <= new_r < self.maze.grid_size and 0 <= new_c < self.maze.grid_size:
                self.player_row = new_r
                self.player_col = new_c

                # Update pixel position of player
                half = self.maze.cell_size // 2
                self.player_position = (
                    self.maze.offset_x + new_c * self.maze.cell_size + half - self.player_sprite.get_width() // 2,
                    self.maze.offset_y + new_r * self.maze.cell_size + half - self.player_sprite.get_height() // 2
                )
        if dx != 0 or dy != 0:
            print(f"Trying to move {dx},{dy} from ({self.player_row},{self.player_col})")
            print(f"Current connections: {self.maze.grid_connections.get(current_cell, 'EMPTY')}")

if __name__ == "__main__":
    # Dummy objects for testing
    
    dummy_sprite = pygame.Surface((10, 10))
    dummy_sprite.fill((255, 100, 100))          # red square as player

    level = Level(display, None, font, dummy_sprite)
    running = True
          
    while running:
        level.update() # update the level state based on input
        level.draw()
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