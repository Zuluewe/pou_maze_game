# controller 
# takes input from player, manages colission and level progression

import pygame
from level import Level
import screenvariable

# import views
import start as Start
import pause as Pause
import game_over as End
import level as Level

# import models
import food as Food
import time_bonus as timer
import player

class Game:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((screenvariable.SCREENWIDTH, screenvariable.SCREENHEIGHT))
        pygame.display.set_caption("Pou Maze Game")
        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font("assets/PouFont.ttf", 32)
        self.gameStateManager = GameStateManager("Start")
        
        # Create player
        player_sprite = pygame.image.load("assets/images/pou_hungry.png").convert_alpha()
        self.player = player.Player((screenvariable.SCREENWIDTH // 2, screenvariable.SCREENHEIGHT // 2), player_sprite)

        # font
        self.font = pygame.font.Font("assets/PouFont.ttf", 32)
        
        # Create views and pass player sprite
        self.start = Start.Start(self.display, self.gameStateManager, self.font, self.player.sprite)
        self.level = Level.Level(self.display, self.gameStateManager, self.font, self.player.sprite)
        self.pause = Pause.Pause(self.display, self.gameStateManager, self.font, self.player.sprite)
        self.game_over = End.GameOver(self.display, self.gameStateManager, self.font, self.player.sprite)

        self.states = {
            "Start": self.start, 
            "Level": self.level, 
            "Pause": self.pause,
            "GameOver": self.game_over
        }

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # lets player quit by clciking exit button
                    running = False

                self.handle_input(event) # lets you manage game state with input
            
            # draw current view
            current_view = self.states[self.gameStateManager.get_states()]
            current_view.draw(self)
            
            pygame.display.update()
            self.clock.tick(screenvariable.FPS)
        
        pygame.quit()
    
    def handle_input(self, event):
        current_state = self.gameStateManager.get_states()
        
        if current_state == "Start":
            if event.type == pygame.KEYDOWN: # if you press a key you start the game
                self.gameStateManager.set_states("Level")
        
        elif current_state == "Level":  # if you press escape on level you pause
            if event.type == event.key == pygame.K_ESCAPE:
                self.gameStateManager.set_states("Pause")
        
        elif current_state == "Pause":
            if event.type == pygame.KEYDOWN: # if you press a key on pause menu you go back to the game
                self.gameStateManager.set_states("Level")
            elif event.type == pygame.K_ESCAPE: # if you press escape in pause menu its game over
                self.gameStateManager.set_states("GameOver")

        elif current_state == "GameOver":
            if event.type == event.key == pygame.K_r: # if you click "r" you restart the level
                self.gameStateManager.set_states("Level")

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

