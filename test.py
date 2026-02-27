import pygame

SCREENWIDTH = 1280
SCREENHEIGHT = 720
FPS = 60

# pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT)) # window size
pygame.display.set_caption("Pou Maze Game") # window title
clock = pygame.time.Clock()
running = True
dt = 0 # time


# load player
player_sprite = pygame.image.load("assets/images/pou_hungry.png")
player_width = player_sprite.get_width()
player_height = player_sprite.get_height()

player_position = pygame.Vector2(player_width, screen.get_height() / 2) # position in middle
player_rect = player_sprite.get_rect()


# load food
food_sprite = pygame.image.load("assets/images/Burger.webp")
food_width = food_sprite.get_width()
food_height = food_sprite.get_height()

food_position = pygame.Vector2(screen.get_width() - player_width, screen.get_height() / 2)
food_rect = food_sprite.get_rect()


# font
font = pygame.font.Font("assets/PouFont.ttf", 32)


# sound
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

    # RENDER game objects
    screen.blit(player_sprite, player_position)
    screen.blit(food_sprite, food_position)

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

    # check collision
    if player_rect.colliderect(food_rect):
        pou_eating.play() #eating sound
        food_sprite.fill(0) # food dissapear

    # flip() the display to put your work on screen
    pygame.display.flip()

    dt = clock.tick(FPS) / 1000
    clock.tick(FPS)

pygame.quit()