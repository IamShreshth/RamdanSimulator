import pygame
import random
import time

pygame.init()

# Dimensions and Constants
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vrat Quest")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

large_font = pygame.font.Font(None, 72)

# Load Assets
try:
    bg_surf = pygame.image.load('assets/background.png').convert()
    bg_img = pygame.transform.scale(bg_surf, (WIDTH, HEIGHT))
    
    p_surf = pygame.image.load('assets/player.jpg').convert()
    player_img = pygame.transform.scale(p_surf, (60, 60))

    sat_surf = pygame.image.load('assets/sattvic.png').convert_alpha()
    sattvic_img = pygame.transform.scale(sat_surf, (40, 40))

    junk_surf = pygame.image.load('assets/junk.png').convert_alpha()
    junk_img = pygame.transform.scale(junk_surf, (40, 40))

    nv_surf = pygame.image.load('assets/nonvrat.png').convert_alpha()
    nonvrat_img = pygame.transform.scale(nv_surf, (40, 40))
except Exception as e:
    print(f"Error loading assets: {e}")
    # Fallback placeholders if images fail to load
    bg_img = pygame.Surface((WIDTH, HEIGHT))
    bg_img.fill((135, 206, 235))
    player_img = pygame.Surface((60, 60))
    player_img.fill((0, 0, 255))
    sattvic_img = pygame.Surface((40, 40))
    sattvic_img.fill((0, 255, 0))
    junk_img = pygame.Surface((40, 40))
    junk_img.fill((255, 0, 0))
    nonvrat_img = pygame.Surface((40, 40))
    nonvrat_img.fill((255, 165, 0))

# Game Variables
player_pos = [WIDTH//2 - 30, HEIGHT - 80]
score = 0
vrat_meter = 100
MAX_VRAT = 100

# Item Types
# 0 = Sattvic (+score, +meter)
# 1 = Junk (-meter heavily)
# 2 = Non-Vrat (-score)
items = []
spawn_timer = 0
start_time = time.time()
base_fall_speed = 4

# Game States
MENU = 0
PLAYING = 1
GAME_OVER = 2
state = MENU

def reset_game():
    global player_pos, score, vrat_meter, items, start_time, base_fall_speed
    player_pos = [WIDTH//2 - 30, HEIGHT - 80]
    score = 0
    vrat_meter = 50  # Start with half meter
    items = []
    start_time = time.time()
    base_fall_speed = 4

def draw_vrat_meter(surface, x, y, meter):
    # Background bar
    pygame.draw.rect(surface, (100, 100, 100), (x, y, 200, 20))
    # Fill color depends on meter
    if meter > 60:
        color = (0, 255, 0) # Green
    elif meter > 30:
        color = (255, 255, 0) # Yellow
    else:
        color = (255, 0, 0) # Red
    
    fill_width = max(0, min(200, (meter / MAX_VRAT) * 200))
    if fill_width > 0:
        pygame.draw.rect(surface, color, (x, y, fill_width, 20))
    # Border
    pygame.draw.rect(surface, (255, 255, 255), (x, y, 200, 20), 2)

running = True
while running:
    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if state == MENU or state == GAME_OVER:
                    reset_game()
                    state = PLAYING

    screen.blit(bg_img, (0, 0))

    if state == MENU:
        title = large_font.render("VRAT QUEST", True, (255, 215, 0))
        sub = font.render("Press SPACE to Start", True, (255, 255, 255))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 100))
        screen.blit(sub, (WIDTH//2 - sub.get_width()//2, HEIGHT//2))
        
        # Instructions
        inst1 = font.render("Catch Sattvic (Apple) to maintain Vrat", True, (0, 255, 0))
        inst2 = font.render("Dodge Junk (Burger) - Breaks Vrat!", True, (255, 50, 50))
        inst3 = font.render("Dodge Non-Vrat (Wheat) - Loses Score", True, (255, 165, 0))
        screen.blit(inst1, (WIDTH//2 - inst1.get_width()//2, HEIGHT//2 + 80))
        screen.blit(inst2, (WIDTH//2 - inst2.get_width()//2, HEIGHT//2 + 120))
        screen.blit(inst3, (WIDTH//2 - inst3.get_width()//2, HEIGHT//2 + 160))

    elif state == GAME_OVER:
        title = large_font.render("GAME OVER", True, (255, 50, 50))
        score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
        sub = font.render("Press SPACE to Restart", True, (255, 255, 255))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 100))
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 - 20))
        screen.blit(sub, (WIDTH//2 - sub.get_width()//2, HEIGHT//2 + 40))

    elif state == PLAYING:
        # Controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= 7
        if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - 60:
            player_pos[0] += 7

        # Progressive difficulty
        elapsed_time = time.time() - start_time
        base_fall_speed = 4 + (elapsed_time // 10) * 1  # Increases by 1 every 10s
        spawn_rate = max(20, 60 - int(elapsed_time))  # Spawn faster over time

        # Spawning items
        spawn_timer += 1
        if spawn_timer > spawn_rate:
            spawn_timer = 0
            # Probabilities: 50% Sattvic, 30% Junk, 20% Non-vrat
            rand = random.randint(1, 100)
            if rand <= 50:
                item_type = 0 # Sattvic
            elif rand <= 80:
                item_type = 1 # Junk
            else:
                item_type = 2 # Non-Vrat
            
            x_pos = random.randint(0, WIDTH - 40)
            items.append([x_pos, -40, item_type])

        # Move and Handle items
        for item in items[:]:
            item[1] += base_fall_speed
            
            # Simple collision check
            item_rect = pygame.Rect(item[0], item[1], 40, 40)
            player_rect = pygame.Rect(player_pos[0], player_pos[1], 60, 60)
            
            if item_rect.colliderect(player_rect):
                items.remove(item)
                if item[2] == 0: # Sattvic
                    score += 10
                    vrat_meter = min(MAX_VRAT, vrat_meter + 15)
                elif item[2] == 1: # Junk
                    vrat_meter -= 40
                elif item[2] == 2: # Non-Vrat
                    score = max(0, score - 10)
            elif item[1] > HEIGHT:
                items.remove(item)

        # Check Game Over condition
        if vrat_meter <= 0:
            state = GAME_OVER

        # Drawing
        screen.blit(player_img, (player_pos[0], player_pos[1]))
        
        for item in items:
            if item[2] == 0:
                screen.blit(sattvic_img, (item[0], item[1]))
            elif item[2] == 1:
                screen.blit(junk_img, (item[0], item[1]))
            elif item[2] == 2:
                screen.blit(nonvrat_img, (item[0], item[1]))

        # UI
        score_board = font.render(f"SCORE: {score}", True, (255, 255, 255))
        screen.blit(score_board, (20, 20))
        
        vrat_text = font.render("VRAT METER", True, (255, 255, 255))
        screen.blit(vrat_text, (WIDTH//2 - vrat_text.get_width()//2, 10))
        draw_vrat_meter(screen, WIDTH//2 - 100, 40, vrat_meter)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
