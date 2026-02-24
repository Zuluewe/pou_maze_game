import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720)) # window size
pygame.display.set_caption("Pou Maze Game") # window title
clock = pygame.time.Clock()
running = True

dt = 0 # time

# load player
player_position = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2) # position in middle
player_sprite = pygame.image.load("assets/pou_hungry.png")
player_rect = player_sprite.get_rect

# font
font = pygame.font.Font("assets/PouFont.ttf", 32)


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # background color
    screen.fill("#50b032") # grass green

    # RENDER YOUR GAME HERE

    # blit
    screen.blit(player_sprite, player_position)

    # move player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player_position.y -= 300 * dt

    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player_position.y += 300 * dt

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_position.x += 300 * dt

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_position.x -= 300 * dt

    # flip() the display to put your work on screen
    pygame.display.flip()

    dt = clock.tick(60) / 1000
    clock.tick(60)  # limits FPS to 60

pygame.quit()