import pygame
import sys

SCREENWIDTH = 1280
SCREENHEIGHT = 720
FPS = 60

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        pygame.display.set_caption("Pou Maze Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("assets/PouFont.ttf", 32)

        self.gameStateManager = GameStateManager("Menu")
        self.start = Menu(self.screen, self.gameStateManager, self.font)
        self.level = Level(self.screen, self.gameStateManager, self.font)
        self.pause = Pause_menu(self.screen, self.gameStateManager, self.font)

        self.states = {"Menu": self.start, "Level": self.level, "Pause": self.pause}

    def run(self):
        while True:
            self.states[self.gameStateManager.get_states()].run()

            pygame.display.update()
            self.clock.tick(FPS)


# start menu screen
class Menu:
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
                self.gameState.set_states("Level")



# level screen
class Level:
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



# pause menu screen
class Pause_menu:
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
                self.gameState.set_states("Level")


class GameStateManager:
    def __init__(self, currentState):
        self.currentState = currentState

    def get_states(self):
        return self.currentState
    
    def set_states(self, state):
        self.currentState = state

if __name__ == "__main__":
    game = Game()
    game.run()