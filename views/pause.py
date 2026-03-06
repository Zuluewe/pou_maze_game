# view

import variable

class Pause:
    def __init__(self, display, font, gameStateManager):
        self.display = display
        self.font = font
        self.gameState = gameStateManager

    def draw(self, model):
        self.display.fill("#954d25") # pou dirt
        self.display.blit(self.player_sprite, model.player_position)

        # define text
        pause_text = self.font.render("Game Paused", True, "white")
        return_text = self.font.render("Press any key to continue", True, "white")

        # render text
        self.display.blit(pause_text, (variable.SCREENWIDTH // 2, variable.SCREENHEIGHT // 2))
        self.display.blit(return_text, (variable.SCREENWIDTH // 2, variable.SCREENHEIGHT // 2 - 100))

"""class Pause_menu:
    def __init__(self, display, gameStateManager, font):
        self.display = display
        self.gameState = gameStateManager
        self.font = font
        
    def run(self):
        self.display.fill("#954d25")

    # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            key_press = pygame.key.get_pressed()
            if key_press[pygame.K_ESCAPE]:
                self.gameState.set_states("Level")"""