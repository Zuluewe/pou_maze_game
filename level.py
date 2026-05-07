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
pou_eating = pygame.mixer.Sound("assets/sounds/eat.ogg")
timer = pygame.mixer.Sound("assets/sounds/timer.ogg")
game_over_sound = pygame.mixer.Sound("assets/sounds/game_over.mp3")

class LevelModel:
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

        # define sounds
        self.pou_eating = pou_eating
        self.timer = timer
        self.game_over_sound = game_over_sound

        # TIMER variables
        self.time_left = init_time
        self.time_add = True
        self.game_over = False  # Game over flag
        self.random_number = random.randint(1, 100) # % probability

        #50% chance for timer to apear on every level
        if self.random_number < 50:
            self.time_add = True  # Allow time bonus to be collected
            self.time_sprite.set_alpha(255)  # Make the time bonus sprite visible for this round
        else:
            self.time_add = False  # No time bonus this round
            self.time_sprite.set_alpha(0)  # Make the time bonus sprite invisible for this round
        
        # surface to draw the maze on, so we can blit it to the main display and not have to redraw the maze every frame
        self.maze_surface = pygame.Surface((screenvariable.MAZE_WIDTH , screenvariable.MAZE_WIDTH))
        
        # GENERATE THE MAZE
        self.maze = Maze(self.maze_surface, (self.grid_size), (self.cell_size), screenvariable.OFFSET_X, screenvariable.OFFSET_Y,("#3f5837"))
        self.maze.generate(0,0, self.maze_surface) # generate the maze and draw it directly on the maze surface
        self.move_cooldown = 0.08 # (0,05 = 20 moves / sekund)
        self.move_timer = 0.0 # hold count of the secconds passed so when the cooldown is done the player can move, then it resets to 0

        # PLAYER position (r,c)
        self.player_row = 0
        self.player_col = 0
        half = self.maze.cell_size // 2
        self.player_position = (
            screenvariable.MAZE_START_X + self.player_col * self.maze.cell_size + half - self.player_sprite.get_width() // 2,
            screenvariable.MAZE_START_Y + self.player_row * self.maze.cell_size + half - self.player_sprite.get_height() // 2) # 50 + (0 * 50) + 25 - half of the player sprite = 75, same for y. This centers the player sprite in the cell 
        
        # food and timer position
        self.food_position = ((screenvariable.MAZE_START_X + (self.maze.grid_size - 1) * self.maze.cell_size), (screenvariable.MAZE_START_Y + (self.maze.grid_size -1)*self.maze.cell_size))
        self.time_bonus_position = ((screenvariable.MAZE_START_X + (random.randint(0, self.maze.grid_size -1) * self.maze.cell_size)), (screenvariable.MAZE_START_Y + (random.randint(0, self.maze.grid_size -1) * self.maze.cell_size))) 
    
    # scaling the player sprite size
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

        # Moved COLLISION CHECK in update
        self.check_collision(self.player_position, self.food_position, self.time_bonus_position)

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

        # WASD or arrow keys
        if self.move_timer >= self.move_cooldown:
            if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and 'right' in connections:
                dx = 1
            if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and 'left' in connections:
                dx = -1
            if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and 'down' in connections:
                dy = 1
            if (keys[pygame.K_UP] or keys[pygame.K_w]) and 'up' in connections:
                dy = -1
            
            # if position has changed, position gets redefined
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
        
        
    # function to go the next level
    def next_level(self):
        self.level += 1 # increase the maze size for the next level
        self.grid_size += 2
        self.cell_size = screenvariable.MAZE_WIDTH // self.grid_size
        self.generate_new_maze() # generate a new maze with the updated size

    # function to CREATE next level maze
    def generate_new_maze(self):
        self.maze_surface = pygame.Surface((screenvariable.MAZE_WIDTH , screenvariable.MAZE_WIDTH)) # create a new surface for the new maze
        self.maze = Maze(self.maze_surface, self.grid_size, self.cell_size, screenvariable.OFFSET_X, screenvariable.OFFSET_Y,("#3f5837")) # create a new maze with the updated size
        self.maze.generate(0,0, self.maze_surface)
        #(r,c) coordinates for the player position
        self.player_row = 0
        self.player_col = 0
        #we resize the sprites        
        self.time_sprite = self.scale_sprite(self.time_sprite, self.cell_size, 0.6) # rescale time bonus sprite for the new cell size
        self.food_sprite = self.scale_sprite(self.food_sprite, self.cell_size, 0.8) # rescale food sprite for the new cell size
        self.exit_sprite = self.scale_sprite(self.exit_sprite, self.cell_size, 1) # rescale exit sprite for the new cell size
        self.player_sprite = self.scale_sprite(self.player_sprite, self.cell_size, 0.8) # rescale player sprite for the new cell size
     
        # reset positions
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
        
    # called init to reinitialize level when resetting after game over 
    def reset_level(self):
        
        self.__init__(self.display, self.gameState, self.font, player, self.clock, exit, food, 0, 0, 10, time_sprite) # reinitialize the level with the same level number to reset it

    # COLLISION check
    def check_collision(self, player_position, food_position, time_bonus_position):
        collision_threshold = self.maze.cell_size // 4

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


class LevelView:
    def __init__(self, display, font, clock):
        self.display = display
        self.font = font
        self.clock = clock

    

    def draw(self, model):
        self.display.fill("#50b032")  # grass green
        
        # MAZE
        self.display.blit(model.maze_surface, (screenvariable.MAZE_START_X, screenvariable.MAZE_START_Y))
        model.maze.redraw_paths()
        self.display.blit(model.exit_sprite, (screenvariable.MAZE_START_X - model.maze.cell_size, screenvariable.MAZE_START_Y))
        self.display.blit(model.exit_sprite, (screenvariable.MAZE_START_X + model.maze.grid_size * model.maze.cell_size, screenvariable.MAZE_START_Y + (model.maze.grid_size - 1) * model.maze.cell_size))
        
        # PLAYER
        self.display.blit(model.player_sprite, model.player_position)

        # ASSETS
        self.display.blit(model.food_sprite, model.food_position)
        self.display.blit(model.time_sprite, model.time_bonus_position)        
        
        # TEXT
        font = pygame.font.Font("assets/PouFont.ttf", 32)
        score_text = font.render(f"Score: {model.score}", True, "white")
        time_text = font.render(f"Time: {int(model.time_left)}", True, "white")
        
        self.display.blit(score_text, (10, 10))
        self.display.blit(time_text, (screenvariable.SCREENWIDTH - time_text.get_width() - 10, 10))
        
        pygame.display.flip()


# controller dummy
if __name__ == "__main__":
    pygame.init()
    display = pygame.display.set_mode((screenvariable.SCREENWIDTH, screenvariable.SCREENHEIGHT))
    display.fill("#50b032") # grass green
    pygame.display.set_caption("Pou Maze: Level") # dummy
    font = pygame.font.Font("assets/PouFont.ttf", 32) # dummy
    clock = pygame.time.Clock()
    running = True
    dt = 0

    gameStateManager = 'Level' # dummy
    exit = pygame.image.load("assets/images/exit.jpg").convert_alpha() # Dummy
    time_bonus_sprite = pygame.image.load("assets/images/time.png").convert_alpha() # Dummy
    resized_sprite= pygame.image.load("assets/images/pou_happy.png") # Dummy
    food = pygame.image.load("assets/images/Burger.webp").convert_alpha() # Dummy

    model = LevelModel(display, None, font, resized_sprite, clock, exit, food, 0, 0, 60, time_bonus_sprite) # pass dummy sprite and clock for testing
    level = LevelView(display, font, clock) # pass the model to the view for drawing
    running = True
    
    while running:
        dt = clock.tick(screenvariable.FPS) / 1000.0  # delta time in seconds
        model.update(dt)  # update game state
        level.draw(model)  # render the updated model

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()