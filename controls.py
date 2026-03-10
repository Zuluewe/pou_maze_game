# controller 
# takes input from player, manages colission and level progression

import pygame

import views.variable

# import views
import views.start as Start
import views.pause as Pause
import views.game_over as End
import views.level as Level

# import models
import models.food as Food
import models.time_bonus as timer
import models.player as player

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((variable.SCREENWIDTH, variable.SCREENHEIGHT))
        pygame.display.set_caption("Pou Maze Game")
        self.clock = pygame.time.Clock()

        # font
        self.font = pygame.font.Font("assets/PouFont.ttf", 32)

        self.gameStateManager = GameStateManager("Menu")
        self.start = Start(self.screen, self.gameStateManager, self.font)
        self.level = Level(self.screen, self.gameStateManager, self.font)
        self.pause = Pause(self.screen, self.gameStateManager, self.font)
        self.pause = End(self.screen, self.gameStateManager, self.font)

        self.states = {"Menu": self.start, "Level": self.level, "Pause": self.pause}

    def run(self):
        while True:
            self.states[self.gameStateManager.get_states()].run()

            pygame.display.update()
            self.clock.tick(FPS)

class GameState:
    def __init__(self):
        self.score = 0
        self.time_left = 10 # should be 60 seconds
        self.game_over = False

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

    