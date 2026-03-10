# view

import screenvariable

class GameOver:
    def __init__(self, display, font, gameStateManager, player_sprite):
        self.display = display
        self.font = font
        self.gameState = gameStateManager
        self.player_sprite = player_sprite

    def draw(self, model):
        self.display.fill("#50b032") # pou grass green
        self.display.blit(self.player_sprite, model.player_position)

        # define text
        game_over_text = self.font.render("Game Over", True, "white")
        restart_game_text = self.font.render("Press 'r' to restart game", True, "white")

        # render text
        self.display.blit(game_over_text, (10, 10))
        self.display.blit(restart_game_text, (10, 20))

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