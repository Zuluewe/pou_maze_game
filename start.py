# view

import pygame
import screenvariable

class Start:
    def __init__(self, display, font, gameStateManager, player_sprite = None):
        self.display = display
        self.font = font
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
        pygame.draw.rect(self.display, "#50b032", (0, screenvariable.SCREENHEIGHT - 250, screenvariable.SCREENWIDTH, 250)) # screen, color, x position, y position, square width, square height
        self.display.blit(background_picture, (0, screenvariable.SCREENHEIGHT - 175 - background_picture_height)) # picture, x position, y position

        self.display.blit(player_sprite, (screenvariable.SCREENWIDTH / 2 - player_sprite_width / 2, (screenvariable.SCREENHEIGHT / 3) * 2))
        
        self.display.blit(welcome_text, (((screenvariable.SCREENWIDTH - welcome_text_width) // 2, screenvariable.SCREENHEIGHT // 2 - 250))) # display welcome text
        self.display.blit(start_text, (((screenvariable.SCREENWIDTH - start_text_width) // 2, screenvariable.SCREENHEIGHT // 2 - 150))) # display start text

# controller
if __name__ == "__main__":
    pygame.init()
    gameStateManager = 'Start' # dummy for testing, should be passed from Game class
    screen = pygame.display.set_mode((screenvariable.SCREENWIDTH, screenvariable.SCREENHEIGHT ))
    pygame.display.set_caption("Pou Maze Game: Start")
    clock = pygame.time.Clock()
    running = True
    font = pygame.font.Font("assets/PouFont.ttf", 32)
    player_sprite = pygame.image.load("assets/images/pou_happy.png")
    
    start_view = Start(screen, font, gameStateManager, player_sprite) # dummy font and gameStateManager for testing, should be passed from Game class
    
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
        clock.tick(screenvariable.FPS)
    pygame.quit()

