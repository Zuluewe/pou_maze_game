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
running = True
dt = 0

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
        self.maze_surface = pygame.Surface((MAZE_WIDTH, MAZE_WIDTH))
        self.maze = maze_generator.Maze(self.display, GRID_SIZE, CELL_SIZE, OFFSET_X, OFFSET_Y,("#3f5837"))
        self.maze.generate(0,0) # generate the maze and draw it directly on the display
        
        

        self.move_cooldown = 0.20 #seconds between moves (0,20 = 5 moves/sec)
        self.move_timer = 0.0
    #player start
        half = self.maze.cell_size // 2
        self.player_position = (
            self.maze.offset_x + self.player_col * self.maze.cell_size + half - self.player_sprite.get_width() // 2,
            self.maze.offset_y + self.player_row * self.maze.cell_size + half - self.player_sprite.get_height() // 2
        
        ) # 50 + (0 * 50) + 25 - half of the player sprite = 75, same for y. This centers the player sprite in the cell 

        
        self.draw() # draw the initial state of the level      

    def draw(self):  
            
        
        self.maze.redraw_paths(target_screen=self.display)
        self.display.blit(self.player_sprite, self.player_position)
        # define text
        score_text = font.render(f"Score: 0", True, "white")
        # render text
        self.display.blit(score_text, (10, 10))
        pygame.display.flip() # update the display after drawing everything
        
    def update(self, dt):
        self.move_timer += dt

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        current_cell = (self.player_row, self.player_col)
        connections = self.maze.grid_connections.get(current_cell, set())


        if self.move_timer >= self.move_cooldown:
            if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and 'right' in connections:
                dx = 1
            if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and 'left' in connections:
                dx = -1
            if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and 'down' in connections:
                dy = 1
            if (keys[pygame.K_UP] or keys[pygame.K_w]) and 'up' in connections:
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
                self.move_timer = 0.0  # reset timer after move
        

if __name__ == "__main__":
    # Dummy objects for testing
    
    dummy_sprite = pygame.Surface((10, 10))
    dummy_sprite= pygame.image.load("assets/images/pou_happy.png")  
    rezized_sprite = pygame.transform.smoothscale(dummy_sprite, (CELL_SIZE -10, CELL_SIZE - 10))

    level = Level(display, None, font, rezized_sprite)
    running = True
          
    while running:
        dt = clock.tick(60) / 1000.0
        level.update(dt) # update the level state based on input
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