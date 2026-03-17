# view
import pygame 
import screenvariable

class GameOver:
    def __init__(self, display, font, gameStateManager, player_sprite = None):
        self.display = display
        self.font = font
        self.gameState = gameStateManager
        self.player_sprite = player_sprite

    def draw(self, model):
        self.display.fill("#3690df") # dark grass

        # font
        game_over_font = pygame.font.Font("assets/PouFont.ttf", 62)
        pou_died_font = pygame.font.Font("assets/PouFont.ttf", 32)
        font = pygame.font.Font("assets/PouFont.ttf", 32)

        # define
        background_picture = pygame.image.load("assets/images/forest_1.png").convert_alpha()
        
        game_over_text = game_over_font.render("Game Over", True, "white")
        pou_died_text = font.render("Pou starved to death", True, "red")
        score_text = font.render(f"Score:", True, "white")
        restart_game_text = font.render("Press 'r' to restart game", True, "white")

        # get size
        background_picture_height = background_picture.get_height()

        game_over_text_width = game_over_text.get_width()
        pou_died_text_width = pou_died_text.get_width()
        score_text_width = score_text.get_width()
        restart_game_text_width = restart_game_text.get_width()

        # render text
        self.display.blit(background_picture, (0, screenvariable.SCREENHEIGHT - background_picture_height + 35)) # picture, x position, y position

        self.display.blit(game_over_text, (((screenvariable.SCREENWIDTH - game_over_text_width) // 2, screenvariable.SCREENHEIGHT // 2 - 250))) # display game over
        self.display.blit(pou_died_text, (((screenvariable.SCREENWIDTH - pou_died_text_width) // 2, screenvariable.SCREENHEIGHT // 2 - 125))) # display death
        self.display.blit(score_text, (((screenvariable.SCREENWIDTH - score_text_width) // 2, screenvariable.SCREENHEIGHT // 2 - 25)))
        self.display.blit(restart_game_text, (((screenvariable.SCREENWIDTH - restart_game_text_width) // 2, screenvariable.SCREENHEIGHT // 2 + 75)))

# controller
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((screenvariable.SCREENWIDTH, screenvariable.SCREENHEIGHT))
    pygame.display.set_caption("Pou Maze Game: Start")
    clock = pygame.time.Clock()
    running = True
    
    game_over_view = GameOver(screen, None)
    
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