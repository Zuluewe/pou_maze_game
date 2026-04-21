# view

import pygame
#from maze_generator import Maze
#from views.maze_generator import Maze

import maze_generator
import screenvariable
import time_bonus
import food

class Level:
    def __init__(self, display, gameStateManager, font, player_sprite, clock):
        self.clock = clock # local clock for the level, so it can control its own timing without affecting the main game loop
        self.display = display
        self.font = font
        self.gameState = gameStateManager
        self.player_sprite = player_sprite

    #(r,c) coordinates for the player position
        self.player_row = 0
        self.player_col = 0
        self.maze_surface = pygame.Surface((screenvariable.MAZE_WIDTH, screenvariable.MAZE_WIDTH)) # surface to draw the maze on, so we can blit it to the main display and not have to redraw the maze every frame
    
    # generate the maze once during initialization
        self.maze = maze_generator.Maze(self.maze_surface, screenvariable.GRID_SIZE, screenvariable.CELL_SIZE, screenvariable.OFFSET_X, screenvariable.OFFSET_Y,("#3f5837"))
        self.maze.generate(0,0, self.maze_surface) # generate the maze and draw it directly on the display
        self.move_cooldown = 0.05 #seconds between moves (0,20 = 5 moves/sec)
        self.move_timer = 0.0
    
    #player start
        half = self.maze.cell_size // 2
        self.player_position = (
            screenvariable.MAZE_START_X + self.player_col * self.maze.cell_size + half - self.player_sprite.get_width() // 2,
            screenvariable.MAZE_START_Y + self.player_row * self.maze.cell_size + half - self.player_sprite.get_height() // 2
        
        ) # 50 + (0 * 50) + 25 - half of the player sprite = 75, same for y. This centers the player sprite in the cell 
        
        self.draw() # draw the initial state of the level      

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
                        screenvariable.MAZE_START_X + new_c * self.maze.cell_size + half - self.player_sprite.get_width() // 2,
                        screenvariable.MAZE_START_Y + new_r * self.maze.cell_size + half - self.player_sprite.get_height() // 2 
                    )
                self.move_timer = 0.0  # reset timer after move

    def draw(self, model=None):  
        self.display.fill("#50b032") # grass green
        self.display.blit(self.maze_surface, (screenvariable.MAZE_START_X, screenvariable.MAZE_START_Y)) # blit the pre-drawn maze surface onto the main display
        font = pygame.font.Font("assets/PouFont.ttf", 32)
        self.maze.redraw_paths() # redraw the maze paths on top of the maze surface, so they are visible above the walls # redraw entrance and exit to make sure they are visible above the paths
        self.display.blit(self.player_sprite, self.player_position)

        # define text
        score_text = font.render(f"Score: 0", True, "white")
        time_text = font.render(f"Time: 0", True, "white")


        # render text
        self.display.blit(score_text, (10, 10))
        self.display.blit(time_text, (screenvariable.SCREENWIDTH - time_text.get_width() - 10, 10))

        pygame.display.flip() # update the display after drawing everything
        dt = self.clock.tick(screenvariable.FPS) / 800.0
        self.update(dt)    

if __name__ == "__main__":
    # Dummy objects for testing
    pygame.init()
    display = pygame.display.set_mode((screenvariable.SCREENWIDTH, screenvariable.SCREENHEIGHT))
    display.fill("#50b032") # grass green
    pygame.display.set_caption("Level")
    font = pygame.font.Font("assets/PouFont.ttf", 32)
    clock = pygame.time.Clock()
    running = True
    dt = 0
    gameStateManager = 'Level' # dummy for testing, should be passed from Game class
    
    dummy_sprite= pygame.image.load("assets/images/pou_happy.png")  
    rezized_sprite = pygame.transform.smoothscale(dummy_sprite, (screenvariable.CELL_SIZE -10, screenvariable.CELL_SIZE - 10))

    level = Level(display, None, font, rezized_sprite, clock) # pass dummy sprite and clock for testing
    running = True
    
    while running:
        level.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        clock.tick(screenvariable.FPS)
    pygame.quit()