import pygame

SCREENWIDTH = 1280
SCREENHEIGHT = 720
FPS = 60
food_eaten = False
time_add = False

# pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT)) # window size
pygame.display.set_caption("Pou Maze Game") # window title
clock = pygame.time.Clock()
running = True
dt = 0 # time
score = 0

# inbuilt timer
time_elapsed = 10

# load player
player_sprite = pygame.image.load("assets/images/pou_hungry.png")
player_width = player_sprite.get_width()
player_height = player_sprite.get_height()

player_position = pygame.Vector2(player_width, screen.get_height() / 2) # position in middle
player_rect = player_sprite.get_rect()

# load food
food_sprite = pygame.image.load("assets/images/Burger.webp")
food_position = pygame.Vector2((SCREENWIDTH - player_width), SCREENHEIGHT / 2)
food_rect = food_sprite.get_rect()

# load stopwatch
time_sprite = pygame.image.load("assets/images/time.png")
time_position = pygame.Vector2((SCREENWIDTH / 2, SCREENHEIGHT / 2))
time_rect = time_sprite.get_rect()


# font and load text
font = pygame.font.Font("assets/PouFont.ttf", 32)

score_text = font.render(f"Score: {score}", True, "white")
time_text = font.render(f"Time: {time_elapsed}", True, "white")
game_over_text = font.render("Game Over", True, "white")
restart_game_text = font.render("Press 'r' to restart game", True, "white")

# load sound
background_music = pygame.mixer.music.load("assets/sounds/background_music.ogg")
pygame.mixer.music.play(-1, 0.0) # -1 means the music loops forever and the next varible is where the song starts
pygame.mixer.music.set_volume(0.1)  

pou_eating = pygame.mixer.Sound("assets/sounds/pou_eating.mp3")
game_over = pygame.mixer.Sound("assets/sounds/game_over.mp3")


# main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False    

    screen.fill("#50b032") # grass green

    # render text
    screen.blit(score_text, (10, 10))
    
    # timer
    screen.blit(time_text, (SCREENWIDTH - time_text.get_width() - 10, 10))

    time_elapsed -= dt
    time_text = font.render(f"Time: {int(time_elapsed)}", True, "white")  # Update text each frame
    screen.blit(time_text, (SCREENWIDTH - time_text.get_width() - 10, 10))

    # game over logic
    if time_elapsed <= 0:
        screen.blit(game_over_text, ((SCREENWIDTH - game_over_text.get_width()) // 2, (SCREENHEIGHT - game_over_text.get_height()) // 2))
        screen.blit(restart_game_text, (SCREENWIDTH // 2 - game_over_text.get_width() // 2, (SCREENHEIGHT + game_over_text.get_height() - restart_game_text.get_height() + 100) // 2))
        pygame.mixer.music.stop()

        # check for restart
        if keys[pygame.K_r]:
            score = 0
            time_elapsed = 10
            score_text = font.render(f"Score: {score}", True, "white")
            time_text = font.render(f"Time: {int(time_elapsed)}", True, "white")

            pygame.mixer.music.play(-1, 0.0) # -1 means the music loops forever and the next varible is where the song starts
            pygame.mixer.music.set_volume(0.1) 

    # RENDER game objects
    screen.blit(player_sprite, player_position)

    if not food_eaten:
        screen.blit(food_sprite, food_position)

    if not time_add:
        screen.blit(time_sprite, time_position)

    # move player
    keys = pygame.key.get_pressed() 
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and player_position.y > 0: # move up but withing frame
        player_position.y -= 300 * dt

    if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player_position.y < SCREENHEIGHT - player_height: # move down but within frame (frame - player height)
        player_position.y += 300 * dt

    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_position.x < SCREENWIDTH - player_width: # move right but withing frame
        player_position.x += 300 * dt

    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_position.x > 0: # move left but within frame (frame - player width)
        player_position.x -= 300 * dt

    #update player position
    player_rect.topleft = player_position
    food_rect.topleft = food_position
    time_rect.topleft = time_position

    # check collision food
    if not food_eaten and player_rect.colliderect(food_rect):
        score_text = font.render(f"Score: {score + 1}", True, "white") # score update
        pou_eating.play() #eating sound
        food_eaten = True
        food_sprite.fill(0) # food dissapear
        player_sprite = pygame.image.load("assets/images/pou_happy.png")

    # check collision time
    if not time_add and player_rect.colliderect(time_rect):
        time_elapsed += 5 # add 5 seconds
        time_text = font.render(f"Time: {int(time_elapsed)}", True, "white")
        time_add = True
        time_sprite.fill(0)

# TODO:
# make the world reset with new food in a list (different types of food wow)
# save score


    # flip() the display to put your work on screen
    pygame.display.flip()

    dt = clock.tick(FPS) / 1000

pygame.quit()