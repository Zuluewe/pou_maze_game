import pygame
import random


CELL_SIZE = 50
GRID_SIZE = 5
OFFSET_X = 150
OFFSET_Y = 150
MAZE_WIDTH = GRID_SIZE * CELL_SIZE


# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class Maze():
    def __init__(self, screen, grid_size, cell_size, offset_x, offset_y, color):
        #we initialize the parameters:
        # the grid size is the number of cells, the cell size is in pixels, and the offsets are where the maze starts on the screen. 
        self.screen = screen
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.color = color 
        self.visited = set()
        self.stack = []
        self.solution = {}
        self.grid_connections ={} # this is a dictionary that will store the connections between cells like cell_coords(x,y): [list of connected cell coords]. 
        # initial drawing
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                self.grid_connections[(r,c)] = set() # we initialize the grid connections with empty sets for each cell, we will add to these sets as we remove walls between cells to kep track of where walls are.

    def locate_cell_corners(self, row, col):
        x = self.offset_x + col * self.cell_size # we start at the offset coords:(20,20) + the number of cells we have to move to the right (col) * the size of each cell
        y = self.offset_y + row * self.cell_size #the same for row but we move down instead of right
        return x, y
    
    def draw_grid(self, target_screen = None):
        draw_surface = target_screen if target_screen is not None else self.screen
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x, y = self.locate_cell_corners(row, col)
                pygame.draw.rect(draw_surface, WHITE, (x - 1, y - 1, self.cell_size + 1, self.cell_size + 1), 1) 
                # x,y is where it starts, then we draw a line of length cell_size in both directions to create the cell

    def draw_cell(self, row, col, color, target_screen = None):
        draw_surface = target_screen if target_screen is not None else self.screen
        x, y = self.locate_cell_corners(row, col)
        pygame.draw.rect(draw_surface, color, (x + 1, y + 1, self.cell_size -2, self.cell_size -2)) # we draw a rectangle that is slightly smaller than the cell to create a border effect
    
    def remove_wall(self, row, col, direction, color, target_screen = None):
        draw_surface = target_screen if target_screen is not None else self.screen
        x,y = self.locate_cell_corners(row, col)

        if direction == 'right':
            opposite = 'left'
            pygame.draw.line(draw_surface, color, (x + self.cell_size , y + 1 ), (x + self.cell_size, y + self.cell_size - 1.5), 4) # We draw over the line to make like it is erased
        elif direction == 'left':
            opposite = 'right'
            pygame.draw.line(draw_surface, color, (x, y +1 ), (x, y + self.cell_size -1.5),4)
        elif direction == 'down':
            opposite = 'up'
            pygame.draw.line(draw_surface, color, (x +1, y + self.cell_size), (x + self.cell_size - 1.5, y + self.cell_size), 4)
        elif direction == 'up':
            opposite = 'down'
            pygame.draw.line(draw_surface, color, (x +1 , y), (x + self.cell_size - 1.5, y), 4)

        next_row = row + {'right': 0, 'left': 0, 'down': 1, 'up': -1}[direction]  # new_row is the currentRow + 1 if we go down or -1 if we go up, and it stays the same if we go right or left
        next_col = col + {'right': 1, 'left': -1, 'down': 0, 'up': 0}[direction] # we are saying it has to chose an object from the dictionary we just created baseed on the direection

        self.grid_connections[(row, col)].add(direction) 
        self.grid_connections[(next_row, next_col)].add(opposite)
        

    def generate(self, start_row= 0, start_col =0):
        # local clock so we don't rely on a globalĸ
        clock = pygame.time.Clock()
        self.stack.append((start_row, start_col))
        self.visited.add((start_row, start_col))

        while self.stack: # while len(self.stack) > 0
            row, col = self.stack[-1] # we look at the top of the stack but we dont pop it yet because we might need to backtrack
            neighbors = []
            directions = [
                          (row, col + 1, 'right'),
                          (row, col - 1, 'left'), 
                          (row + 1, col, 'down'), 
                          (row - 1, col, 'up')
                          ] # notice how cordinates are placed in pygame
            
            for neighbor_row, neighbor_col, direction  in directions:
                if 0<= neighbor_row < self.grid_size and 0 <= neighbor_col < self.grid_size and (neighbor_row, neighbor_col) not in self.visited: # we check if the neighbor is within the grid and if it has not been visited yet
                    neighbors.append((neighbor_row, neighbor_col, direction))

                    # by adding the direction we avoid nesting too many if else statements

            if neighbors:
                neighbor_row, neighbor_col, direction = random.choice(neighbors) # we randomly choose a neighbor to visit
                self.remove_wall(row, col, direction, self.color, None) # we remove the wall between the current cell and the chosen neighbor
                self.visited.add((neighbor_row, neighbor_col)) # we mark the chosen neighbor as visited
                self.stack.append((neighbor_row, neighbor_col)) # we add the chosen neighbor to the stack to continue the maze generation from there
                self.draw_cell(neighbor_row, neighbor_col, self.color, None) # make the maze path

                self.solution[(neighbor_row, neighbor_col)] = (row, col) # we store this cell in the solution dict saying: before_cell_choords : solution_to_this_cell_coords
                pygame.display.flip()
                clock.tick(120)            
            else:
                self.stack.pop() # if there are no unvisited neighbors we backtrack by popping the stack            
            
        self.open_entrance_and_exit(self.color, None) 
            
    
    def open_entrance_and_exit(self, color, target_screen = None):
        draw_surface = target_screen if target_screen is not None else self.screen
        pygame.draw.line(draw_surface, BLACK, (OFFSET_X, OFFSET_Y), (OFFSET_X + CELL_SIZE, OFFSET_Y), 5)
        exit_x = OFFSET_X + (GRID_SIZE - 1) * CELL_SIZE
        exit_y = OFFSET_Y + (GRID_SIZE) * CELL_SIZE
        pygame.draw.line(draw_surface, BLACK, (exit_x, exit_y), (exit_x + CELL_SIZE, exit_y), 5)
        self.draw_cell(0, 0, color) # row 0, col 0
        #self.draw_cell(GRID_SIZE-1, GRID_SIZE - 1, GREEN)
        
        pygame.display.flip()
        clock = pygame.time.Clock() #again local clock
        clock.tick(60)
        #print(f'connections: {self.grid_connections}')



# this is so it can be tested
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((600, 700))
    screen.fill("#50b032") # pou grass green
    pygame.display.set_caption("Maze Generator")
    clock = pygame.time.Clock()

    maze = Maze(screen, GRID_SIZE, CELL_SIZE, OFFSET_X, OFFSET_Y,("#434d3f"))
    
    maze.generate(0, 0)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        clock.tick(60)
    pygame.quit()


    