# view

import pygame
import variable

class Start:
    def __init__(self, display, gameStateManager, player_sprite = None):
        self.display = display
        self.gameState = gameStateManager
        self.player_sprite = player_sprite

    def draw(self, model):
        self.display.fill("#3690df") # pou sky green

        # font
        welcome_font = pygame.font.Font("assets/PouFont.ttf", 62)
        font = pygame.font.Font("assets/PouFont.ttf", 32)
        
        # define
        welcome_text = welcome_font.render("Pou Maze Game", True, "white")
        start_text = font.render("Press any key to start", True, "white")
        background_picture = pygame.image.load("assets/images/forest_1.png").convert_alpha()
        player_sprite = pygame.image.load("assets/images/pou_happy.png")

        # get size
        welcome_text_width = welcome_text.get_width()
        start_text_width = start_text.get_width()
        background_picture_height = background_picture.get_height()
        player_sprite_width = player_sprite.get_width()
        
        # render
        pygame.draw.rect(self.display, "#50b032", (0, variable.SCREENHEIGHT - 250, variable.SCREENWIDTH, 250)) # screen, color, x position, y position, square width, square height
        self.display.blit(background_picture, (0, variable.SCREENHEIGHT - 175 - background_picture_height)) # picture, x position, y position

        self.display.blit(player_sprite, (variable.SCREENWIDTH / 2 - player_sprite_width / 2, (variable.SCREENHEIGHT / 3) * 2))
        
        self.display.blit(welcome_text, (((variable.SCREENWIDTH - welcome_text_width) // 2, variable.SCREENHEIGHT // 2 - 250))) # display welcome text
        self.display.blit(start_text, (((variable.SCREENWIDTH - start_text_width) // 2, variable.SCREENHEIGHT // 2 - 150))) # display start text

# controller
"""if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((variable.SCREENWIDTH, variable.SCREENHEIGHT))
    pygame.display.set_caption("Pou Maze Game: Start")
    clock = pygame.time.Clock()
    running = True
    
    start_view = Start(screen, None)
    
    class Model:
        pass
    
    model = Model()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                running = False
        
        start_view.draw(model)
        pygame.display.flip()
        clock.tick(variable.FPS)
    pygame.quit()

"""