import pygame
import random

pygame.init()
#Dimensions of the screen and player postioton and all that , Damn nigaa
screen =pygame.display.set_mode((800,600))
player_pos=[400,500]
food_pos=[random.randint(0, 750), 0]
#intial score 
score=0
font = pygame.font.Font(None, 36)
#clock.tick(60) tells Pygame: "Hey, wait a second... make sure this loop only runs 60 times per second.
clock = pygame.time.Clock()
p_surf = pygame.image.load('assets/player.jpg').convert() #image in assest folder

player_img = pygame.transform.scale(p_surf, (50, 50)) # Now player_img is ready to use forever

running = True
while running:
    screen.fill((135, 206, 235))   #Color of the sky DAMNNNNNNN

    #Event Handling
    #1.ON/OFF Screen Close/Open Window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False

    #controls
    keys=pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= 5
    if keys[pygame.K_RIGHT] and player_pos[0] < 750:
        player_pos[0] += 5
    
    #2.Gravity 
    food_pos[1] += 5 # Make the food fall

    # Reset food if it hits bottom or is caught
    if food_pos[1] > 600:
        food_pos = [random.randint(0, 750), 0]
    
    # Simple collision box check
    if (player_pos[0] < food_pos[0] < player_pos[0] + 50) and \
       (player_pos[1] < food_pos[1] < player_pos[1] + 50):
        score += 1
        food_pos = [random.randint(0, 750), 0]

    #score board 
    score_board = font.render(f"SCORE: {score}", True, (255, 255, 255))
    screen.blit(score_board, (10, 10))

    # 3. Rendering (Drawing)
    screen.blit(player_img, (player_pos[0], player_pos[1]))
    pygame.draw.circle(screen, (255, 255, 0), (food_pos[0], food_pos[1]), 15)   # Food
    
    pygame.display.flip()
    clock.tick(60) # Limits to 60 FPS

pygame.quit()

