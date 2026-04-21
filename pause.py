# view

import pygame
import screenvariable

class Pause:
    def __init__(self, display, font, gameStateManager, player_sprite = None):
        self.display = display
        self.font = font
        self.gameState = gameStateManager
        self.player_sprite = player_sprite

    def draw(self, model = None):
        self.display.fill("#954d25") # pou dirt

        # font
        pause_font = pygame.font.Font("assets/PouFont.ttf", 62)
        font = pygame.font.Font("assets/PouFont.ttf", 32)

        # define text
        background_picture = pygame.image.load("assets/images/forest_1.png").convert_alpha()

        pause_text = pause_font.render("Game Paused", True, "white")
        return_text = font.render("Press any key to continue", True, "white")

        # get size
        background_picture_height = background_picture.get_height()

        pause_text_width = pause_text.get_width()
        return_text_width = return_text.get_width()

        # render text
        pygame.draw.rect(self.display, "#3690df", (0, 0, screenvariable.SCREENWIDTH, 250)) # screen, color, x position, y position, square width, square height
        pygame.draw.rect(self.display, "#50b032", (0, 250, screenvariable.SCREENWIDTH, 50)) # screen, color, x position, y position, square width, square height
        self.display.blit(background_picture, (0, (screenvariable.SCREENHEIGHT - background_picture_height) // 10)) # picture, x position, y position

        self.display.blit(pause_text, (((screenvariable.SCREENWIDTH - pause_text_width) // 2, screenvariable.SCREENHEIGHT // 2 ))) # display game over
        self.display.blit(return_text, (((screenvariable.SCREENWIDTH - return_text_width) // 2, screenvariable.SCREENHEIGHT // 2 + 100))) # display death

# controller
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((screenvariable.SCREENWIDTH, screenvariable.SCREENHEIGHT))
    pygame.display.set_caption("Pou Maze Game: Start")
    clock = pygame.time.Clock()
    running = True
    
    game_over_view = Pause(screen, None)
    
    class Model:
        pass
    
    model = Model()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                running = False
        
        game_over_view.draw(model)
        pygame.display.flip()
        clock.tick(screenvariable.FPS)
    pygame.quit()