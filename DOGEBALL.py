import pygame, random, sys

# Initialize Pygame
pygame.init()

# Screen dimensions and setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neon Racer")
clock = pygame.time.Clock()

# Colors and fonts
BG_COLOR = (20, 20, 30)
PLAYER_COLOR = (0, 255, 255)  # Neon cyan for the player
OBSTACLE_COLOR = (255, 50, 50)
PICKUP_COLOR = (50, 255, 50)
ROAD_COLOR = (50, 50, 50)
font = pygame.font.Font(None, 36)

# Game Variables
player_x = WIDTH // 2
player_y = HEIGHT - 120
player_speed = 7
obstacles = []
pickups = []
frame_count = 0
score = 0

# Road variables
road_y = 0
road_speed = 5
obstacle_spawn_rate = 30  # frames

# Main Game Loop
running = True
while running:
    screen.fill(BG_COLOR)
    
    # Draw scrolling road (two sections for continuous scroll)
    road_y += road_speed
    if road_y >= HEIGHT:
        road_y = 0
    pygame.draw.rect(screen, ROAD_COLOR, (200, road_y, 400, HEIGHT))
    pygame.draw.rect(screen, ROAD_COLOR, (200, road_y - HEIGHT, 400, HEIGHT))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 200:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < 540:  # 800 - 260 to keep within road
        player_x += player_speed
    
    # Spawn obstacles
    frame_count += 1
    if frame_count % obstacle_spawn_rate == 0:
        x = random.randint(220, 580)
        obstacles.append([x, -50, random.randint(4, 7)])
    
    # Spawn pickups occasionally
    if random.randint(1, 200) == 1:
        x = random.randint(220, 580)
        pickups.append([x, -30])
    
    # Update obstacles and draw them
    for obstacle in obstacles[:]:
        obstacle[1] += obstacle[2]
        obs_rect = pygame.Rect(obstacle[0], obstacle[1], 40, 40)
        pygame.draw.rect(screen, OBSTACLE_COLOR, obs_rect)
        if obstacle[1] > HEIGHT:
            obstacles.remove(obstacle)
    
    # Update pickups and draw them
    for pickup in pickups[:]:
        pickup[1] += 3
        pick_rect = pygame.Rect(pickup[0]-15, pickup[1]-15, 30, 30)
        pygame.draw.ellipse(screen, PICKUP_COLOR, pick_rect)
        if pickup[1] > HEIGHT:
            pickups.remove(pickup)
    
    # Create player rectangle and draw
    player_rect = pygame.Rect(player_x, player_y, 60, 30)
    pygame.draw.rect(screen, PLAYER_COLOR, player_rect)
    
    # Collision detection for obstacles
    for obstacle in obstacles:
        obs_rect = pygame.Rect(obstacle[0], obstacle[1], 40, 40)
        if player_rect.colliderect(obs_rect):
            print("Game Over!")
            running = False
    
    # Collision detection for pickups
    for pickup in pickups[:]:
        pick_rect = pygame.Rect(pickup[0]-15, pickup[1]-15, 30, 30)
        if player_rect.colliderect(pick_rect):
            score += 100  # Bonus for collecting a pickup
            pickups.remove(pickup)
    
    # Update score over time
    score += 1
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()