# view

import pygame
import random
import maze_generator
import screenvariable
from maze_generator import Maze 

# we load the sprites here to pass them to the level class, so we don't have to load them every time we reset the level, which would cause performance issues. We also convert_alpha() to optimize the images for faster blitting with transparency.
player = pygame.image.load("assets/images/pou_happy.png") 
food = pygame.image.load("assets/images/Burger.webp")
exit = pygame.image.load("assets/images/exit.jpg")
time_sprite = pygame.image.load("assets/images/time.png")

class Level:
    def __init__(self, display, gameStateManager, font, player_sprite, clock, exit_sprite, food_sprite, current_level, init_score, init_time, time_bonus_sprite):
        self.level = current_level
        self.grid_size, self.cell_size = self.get_level_config(self.level) # get the grid size and cell size for the current level
        self.clock = clock # for player movement
        self.display = display
        self.font = font
        self.gameState = gameStateManager
        self.player_sprite = self.scale_sprite(player_sprite, self.cell_size, 0.8)
        self.food_sprite = self.scale_sprite(food_sprite, self.cell_size, 0.8)
        self.exit_sprite = self.scale_sprite(exit_sprite, self.cell_size, 1)
        self.time_sprite = self.scale_sprite(time_bonus_sprite, self.cell_size, 0.6)
        self.score = init_score

        self.pou_eating = pygame.mixer.Sound("assets/sounds/eat.ogg")
        self.timer =pygame.mixer.Sound("assets/sounds/timer.ogg")
        self.game_over_sound = pygame.mixer.Sound("assets/sounds/game_over.mp3")


        # TIMER variables
        self.time_left = init_time
        self.time_add = True
        self.game_over = False  # Game over flag
        self.random_number = random.randint(1, 100) # % probability

        if self.random_number < 50:
            self.time_add = True  # Allow time bonus to be collected
            self.time_sprite.set_alpha(255)  # Make the time bonus sprite visible for this round
        else:
            self.time_add = False  # No time bonus this round
            self.time_sprite.set_alpha(0)  # Make the time bonus sprite invisible for this round
            
        self.maze_surface = pygame.Surface((screenvariable.MAZE_WIDTH , screenvariable.MAZE_WIDTH)) # surface to draw the maze on, so we can blit it to the main display and not have to redraw the maze every frame
        
        # GENERATE THE MAZE
        self.maze = Maze(self.maze_surface, (self.grid_size), (self.cell_size), screenvariable.OFFSET_X, screenvariable.OFFSET_Y,("#3f5837"))
        self.maze.generate(0,0, self.maze_surface) # generate the maze and draw it directly on the display
        self.move_cooldown = 0.05 #seconds between moves (0,20 = 5 moves/sec)
        self.move_timer = 0.0

    # PLAYER position (r,c)
        self.player_row = 0
        self.player_col = 0
        half = self.maze.cell_size // 2
        self.player_position = (
            screenvariable.MAZE_START_X + self.player_col * self.maze.cell_size + half - self.player_sprite.get_width() // 2,
            screenvariable.MAZE_START_Y + self.player_row * self.maze.cell_size + half - self.player_sprite.get_height() // 2) # 50 + (0 * 50) + 25 - half of the player sprite = 75, same for y. This centers the player sprite in the cell 
        self.food_position = ((screenvariable.MAZE_START_X + (self.maze.grid_size - 1) * self.maze.cell_size), (screenvariable.MAZE_START_Y + (self.maze.grid_size -1)*self.maze.cell_size))
        self.time_bonus_position = ((screenvariable.MAZE_START_X + (random.randint(0, self.maze.grid_size -1) * self.maze.cell_size)), (screenvariable.MAZE_START_Y + (random.randint(0, self.maze.grid_size -1) * self.maze.cell_size)))
        self.draw()  
    
    # changing the player sprite size
    def scale_sprite(self, sprite, cell_size, proportion):
        size = int(cell_size * proportion)
        return pygame.transform.smoothscale(sprite, (size, size))

    # check how big the maze is
    def get_level_config(self, level):
        grid_size = min(5 + level, 25) # increase grid size for each level, but cap it at 25 to prevent performance issues)
        #time_limit --> could add time limit depending on grid size
        cell_size = screenvariable.MAZE_WIDTH // grid_size
        return grid_size, cell_size

    # updates the game and player position
    def update(self, dt):
        # Decrease time
        self.time_left -= dt
        if self.time_left <= 0:
            self.time_left = 0
            self.game_over_sound.play()
            self.game_over = True
            return 

        self.move_timer += dt # used to control the speed of the player movement, so it doesn't move too fast and glitch when holding down a key

        # PLAYER INPUT
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

    def next_level(self):
        self.level += 1 # increase the maze size for the next level
        self.grid_size += 2
        self.cell_size = screenvariable.MAZE_WIDTH // self.grid_size
        self.generate_new_maze() # generate a new maze with the updated size

    def generate_new_maze(self):
        self.maze_surface = pygame.Surface((screenvariable.MAZE_WIDTH , screenvariable.MAZE_WIDTH)) # create a new surface for the new maze
        self.maze = Maze(self.maze_surface, self.grid_size, self.cell_size, screenvariable.OFFSET_X, screenvariable.OFFSET_Y,("#3f5837")) # create a new maze with the updated size
        self.maze.generate(0,0, self.maze_surface)
        #(r,c) coordinates for the player position
        self.player_row = 0
        self.player_col = 0

        #we reset the positions
        half = self.maze.cell_size // 2
        self.player_position = (
                        screenvariable.MAZE_START_X + self.player_col * self.maze.cell_size + half - self.player_sprite.get_width() // 2,
                        screenvariable.MAZE_START_Y + self.player_row * self.maze.cell_size + half - self.player_sprite.get_height() // 2 
                    )
        self.food_position = ((screenvariable.MAZE_START_X + (self.maze.grid_size - 1) * self.maze.cell_size), (screenvariable.MAZE_START_Y + (self.maze.grid_size -1)*self.maze.cell_size))
        self.time_bonus_position = ((screenvariable.MAZE_START_X + (random.randint(0, self.maze.grid_size -1) * self.maze.cell_size)), (screenvariable.MAZE_START_Y + (random.randint(0, self.maze.grid_size -1) * self.maze.cell_size)))
        self.random_number = random.randint(1, 100) # % probability for time bonus
        if self.random_number < 50:
            self.time_add = True  # Allow time bonus to be collected
            self.time_sprite.set_alpha(255)  # Make the time bonus sprite visible for this round
        else:
            self.time_add = False  # No time bonus this round
            self.time_sprite.set_alpha(0)  # Make the time bonus sprite invisible for this round
        #we resize the sprites        
        self.time_sprite = self.scale_sprite(self.time_sprite, self.cell_size, 0.6) # rescale time bonus sprite for the new cell size
        self.food_sprite = self.scale_sprite(self.food_sprite, self.cell_size, 0.8) # rescale food sprite for the new cell size
        self.exit_sprite = self.scale_sprite(self.exit_sprite, self.cell_size, 1) # rescale exit sprite for the new cell size
        self.player_sprite = self.scale_sprite(self.player_sprite, self.cell_size, 0.8) # rescale player sprite for the new cell size
     
    def reset_level(self):
        
        self.__init__(self.display, self.gameState, self.font, player, self.clock, exit, food, 0, 0, 10, time_sprite) # reinitialize the level with the same level number to reset it

    # COLLISION
    def check_collision(self, player_position, food_position, time_bonus_position):
        collision_threshold = self.maze.cell_size // 2

        # FOOD
        if abs(player_position[0] - food_position[0]) < collision_threshold and abs(player_position[1] - food_position[1]) < collision_threshold:
            self.pou_eating.play()
            new_score = self.score + 1  # increase score and reset level properly
            self.score = new_score
            self.next_level()   # Move to the next level after collecting food

        # TIME BONUS
        if abs(player_position[0]- time_bonus_position[0]) < collision_threshold and abs(player_position[1] - time_bonus_position[1]) < collision_threshold:
            if self.time_add == True: 
                self.timer.play()
                self.time_left += 5 # Ensure time bonus is only collected once per bonus
                self.time_add = False  # Ensure time bonus is only collected once
                self.time_sprite.set_alpha(0)  # Make the time bonus sprite invisible after collection

            else:
                self.time_left = self.time_left  # No change if already collected

    # DRAW THE STAGE
    def draw(self, model=None):  
        self.display.fill("#50b032") # grass green
        self.display.blit(self.maze_surface, (screenvariable.MAZE_START_X, screenvariable.MAZE_START_Y)) # blit the pre-drawn maze surface onto the main display
        font = pygame.font.Font("assets/PouFont.ttf", 32)
        self.maze.redraw_paths() # redraw the maze paths on top of the maze surface, so they are visible above the walls # redraw entrance and exit to make sure they are visible above the paths
        self.display.blit(self.exit_sprite, (screenvariable.MAZE_START_X - (self.maze.cell_size), screenvariable.MAZE_START_Y )) # draw exit on top of paths to make sure it's visible
        self.display.blit(self.exit_sprite, (screenvariable.MAZE_START_X + (self.maze.grid_size) * self.maze.cell_size, screenvariable.MAZE_START_Y + (self.maze.grid_size - 1) * self.maze.cell_size)) # draw exit on top of paths to make sure it's visible
        self.display.blit(self.food_sprite, (self.food_position)) # draw food on top of paths to make sure it's visible
        self.display.blit(self.time_sprite, (self.time_bonus_position)) # draw time bonus on top of paths to make sure it's visible, random position for testing
    
        # Draw player
        self.display.blit(self.player_sprite, self.player_position)
        self.check_collision(self.player_position, self.food_position, self.time_bonus_position) # check for collisions with food and time bonus after drawing the player, so it updates the score and time correctly before rendering the text

        # define text
        score_text = font.render(f"Score: {self.score}", True, "white")
        time_text = font.render(f"Time: {int(self.time_left)}", True, "white")

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
    exit = pygame.image.load("assets/images/exit.jpg").convert_alpha()
    time_bonus_sprite = pygame.image.load("assets/images/time.png").convert_alpha()
    resized_sprite= pygame.image.load("assets/images/pou_happy.png")  
    food = pygame.image.load("assets/images/Burger.webp").convert_alpha()

    level = Level(display, None, font, resized_sprite, clock, exit, food, 0, 0, 10, time_bonus_sprite) # pass dummy sprite and clock for testing
    running = True
    
    while running:
        level.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        clock.tick(screenvariable.FPS)
    pygame.quit()