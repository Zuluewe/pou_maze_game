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
        self.exit = pygame.image.load("assets/images/exit.jpg").convert_alpha()
        self.food = pygame.image.load("assets/images/Burger.webp").convert_alpha()
        time_bonus_sprite = pygame.image.load("assets/images/time.png").convert_alpha()
    

        self.player = player.Player((screenvariable.SCREENWIDTH // 2, screenvariable.SCREENHEIGHT // 2), player_sprite)

        # font
        self.font = pygame.font.Font("assets/PouFont.ttf", 32)

        # music
        background_music = pygame.mixer.music.load("assets/sounds/background_music.ogg")
        pygame.mixer.music.play(-1, 0.0) # -1 means the music loops forever and the next varible is where the song starts
        pygame.mixer.music.set_volume(0.1)

        game_over_sound = pygame.mixer.Sound("assets/sounds/game_over.mp3")
        
        # Create views and pass player sprite
        self.start = Start.Start(self.display, self.gameStateManager, self.font, self.player.sprite)
        self.level = Level.Level(self.display, self.gameStateManager, self.font, self.player.sprite, self.clock, self.exit, self.food, 0, 0, 10, time_bonus_sprite) # pass player sprite for movement and collision, also pass clock for timing and exit and food sprites for drawing
        self.pause = Pause.Pause(self.display, self.gameStateManager, self.font, self.player.sprite)
        self.game_over = End.GameOver(self.display, self.gameStateManager, self.font, self.player.sprite, self.level)

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
            
            # Check if game is over in level
            if self.gameStateManager.get_states() == "Level" and self.level.game_over:
                pygame.mixer.music.stop()
                self.gameStateManager.set_states("GameOver")
            
            # draw current view
            current_view = self.states[self.gameStateManager.get_states()]
            if current_view == self.level: # 
                self.display.fill("#50b032") # grass green
                self.level.draw() # pass player for movement and collision
            else:
                current_view.draw(model = None)
            
            pygame.display.update()
            self.clock.tick(screenvariable.FPS)
        
        pygame.quit()
    
    # PLAYER INPUT
    def handle_input(self, event):
        keys = pygame.key.get_pressed() 
        current_state = self.gameStateManager.get_states()
        
        if current_state == "Start":
            if event.type == pygame.KEYDOWN: # if you press a key you start the game
                pygame.event.clear() # clear the event queue to prevent the key press from affecting the level
                self.gameStateManager.set_states("Level")
        
        elif current_state == "Level" and keys[pygame.K_ESCAPE]:  # if you press escape on level you pause
            pygame.mixer.music.stop()
            self.gameStateManager.set_states("Pause")
        
        elif current_state == "Pause" and event.type == pygame.KEYDOWN: # if you press any key you go back to the game
                pygame.mixer.music.play(-1, 0.0)
                pygame.mixer.music.set_volume(0.1)
                self.gameStateManager.set_states("Level")

        elif current_state == "GameOver":
            if keys[pygame.K_r]: # if you click "r" you restart the level
                self.level.reset_level()  # Reset level state
                self.gameStateManager.set_states("Level")
                pygame.mixer.music.play(-1, 0.0)
                pygame.mixer.music.set_volume(0.1)

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

