# view

import controller as CON

class Start:
    def __init__(self, display, font, gameStateManager):
        self.display = display
        self.font = font
        self.gameState = gameStateManager

    def draw(self, model):
        self.display.fill("#3690df") # pou sky green
        self.display.blit(self.player_sprite, model.player_position)

        # define text
        welcome_text = self.font.render("Welcome to the one and only Pou Maze Game", True, "white")
        start_text = self.font.render("Press any key to start", True, "white")

        # render text
        self.display.blit(welcome_text, (CON.SCREENWIDTH // 2, CON.SCREENHEIGHT // 2))
        self.display.blit(start_text, (CON.SCREENWIDTH // 2, CON.SCREENHEIGHT // 2 - 100))

"""class Menu:
    def __init__(self, display, gameStateManager, font):
        self.display = display
        self.gameState = gameStateManager
        self.font = font
    
    def run(self):
        self.display.fill("#3690df") # sky blue
    
    # Text
        start_text = self.font.render("Press any key to start", True, "white")
        self.display.blit(start_text, (SCREENWIDTH // 2, SCREENHEIGHT // 3))

    # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                self.gameState.set_states("Level")"""