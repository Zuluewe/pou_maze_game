import pygame
import random
WIDTH = 800
HEIGHT = 600
CELL_SIZE = 20
GRID_SIZE = 20
OFFSET_X = 50
OFFSET_Y = 50
MAZE_WIDTH = GRID_SIZE * CELL_SIZE

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Generator")
clock = pygame.time.Clock()


class Maze:
    def __init__(self):
        self.grid_size = GRID_SIZE
        self.cell_size = CELL_SIZE
        self.offset_x = OFFSET_X
        self.offset_y = OFFSET_Y

        self.visited = set()
        self.stack = []
        self.solution = {}

        self.draw_grid()

    def locate_cell_corners(self, row, col):
        x = self.offset_x + col * self.cell_size # we start at the offset coords:(20,20) + the number of cells we have to move to the right (col) * the size of each cell
        y = self.offset_y + row * self.cell_size #the same for row but we move down instead of right
        return x, y
    
    def draw_grid(self):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x, y = self.locate_cell_corners(row, col)
                pygame.draw.rect(screen, WHITE, (x - 1, y - 1, self.cell_size + 1, self.cell_size + 1), 1) 
                # x,y is where it starts, then we draw a line of length cell_size in both directions to create the cell

    def draw_cell(self, row, col, color):
        x, y = self.locate_cell_corners(row, col)
        pygame.draw.rect(screen, color, (x + 2, y + 2, self.cell_size - 3, self.cell_size - 3)) # we draw a rectangle that is slightly smaller than the cell to create a border effect
        
    def remove_wall(self, row, col, direction):
        x,y = self.locate_cell_corners(row, col)
        
        if direction == 'right':
            pygame.draw.line(screen, BLACK, (x + self.cell_size, y), (x + self.cell_size, y + self.cell_size), 3) # We draw over the line to make like it is erased
        elif direction == 'left':
            pygame.draw.line(screen, BLACK, (x, y), (x, y + self.cell_size), 3)
        elif direction == 'down':
            pygame.draw.line(screen, BLACK, (x, y + self.cell_size), (x + self.cell_size, y + self.cell_size), 3)
        elif direction == 'up':
            pygame.draw.line(screen, BLACK, (x, y), (x + self.cell_size, y), 3)
    
    def generate(self, start_row= 0, start_col =0):
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
                self.remove_wall(row, col, direction) # we remove the wall between the current cell and the chosen neighbor
                self.visited.add((neighbor_row, neighbor_col)) # we mark the chosen neighbor as visited
                self.stack.append((neighbor_row, neighbor_col)) # we add the chosen neighbor to the stack to continue the maze generation from there
                self.draw_cell(neighbor_row, neighbor_col, BLACK) # make the maze path

                self.solution[(neighbor_row, neighbor_col)] = (row, col) # we store this cell in the solution dict saying: before_cell_choords : solution_to_this_cell_coords
                pygame.display.flip()
                clock.tick(120)            
            else:
                self.stack.pop() # if there are no unvisited neighbors we backtrack by popping the stack            
            
        self.open_entrance_and_exit() 
            
    
    def open_entrance_and_exit(self):

        pygame.draw.line(screen, BLACK, (OFFSET_X, OFFSET_Y), (OFFSET_X + CELL_SIZE, OFFSET_Y), 5)
        exit_x = OFFSET_X + (GRID_SIZE - 1) * CELL_SIZE
        exit_y = OFFSET_Y + (GRID_SIZE) * CELL_SIZE
        pygame.draw.line(screen, BLACK, (exit_x, exit_y), (exit_x + CELL_SIZE, exit_y), 5)
        self.draw_cell(0, 0, YELLOW) # row 0, col 0
        self.draw_cell(GRID_SIZE-1, GRID_SIZE - 1, GREEN)
        
        pygame.display.flip()
        clock.tick(60)


        

maze = Maze()
maze.draw_grid()
maze.generate(0,0)

running = True
while running:
    # process input (events)
    for event in pygame.event.get():
        # check for closing the window
        if event.type == pygame.QUIT:
            running = False
    pygame.display.set_caption(f"Pow's Dungeon Escape - Maze Generated! (Cells visited: {len(maze.visited)})")
    clock.tick(60)
pygame.quit()


    