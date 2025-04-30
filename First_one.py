import pygame
import random
import math
from pygame import mixer

#Initialize the object
pygame.init()

# Create the screen (Width,height)
screen = pygame.display.set_mode((800,600))

# Adding the caption
pygame.display.set_caption("Space Invader")


# Adding the background image
background = pygame.image.load('Background.png')

# Adding the background sound
mixer.music.load('background.wav')
mixer.music.play(-1)


#Adding the icon
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)


# Bullet
# Ready you can't see the bullet
# Fire The bullet is moving
bulletimg=pygame.image.load('bullet.png')
bulletX = 0
bulletY = 530
bulletX_change = 0
bulletY_change = 15
bullet_state = "ready"


# Enemy Multiples
Enemyimg=[]
enemyX = []
enemyY = []
enemyX_change=[]
enemyY_change=[]
num_of_enemies = 6
for i in range(num_of_enemies):
    Enemyimg.append(pygame.image.load('Enemy.png'))
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(5)
    enemyY_change.append(30)

# Player
playerimg=pygame.image.load('player.png')
playerX = 370
playerY = 530
playerX_change = 0
playerY_change = 3

# Score
score_value = 0
font = pygame.font.Font('Backso.ttf',25)
textX = 10
textY = 10

# Game Over
Over_font = pygame.font.Font('Backso.ttf',64)

def show_score(x,y):
    score=font.render("Score : " + str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

def game_over_text():
    score=Over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(score,(200,250))

def player(x,y):
    screen.blit(playerimg,(x,y))

def Enemy(x,y,i):
    screen.blit(Enemyimg[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg,(x+20,y+10))

def is_collision(enemyX,enemyY,playerX,playerY):
    distance = math.sqrt(math.pow(enemyX-bulletX,2)+math.pow(enemyY-bulletY,2))
    if distance < 27 :
        return True
    else:
        return False




# Game LOOP
running = True
while running:

    # RED_GREEN_BULE
    screen.fill((0,0,0))
    # For Background
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running = False

    # If ketstroke is pressed it pressed it move whether it is right or left
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                playerX_change = -5
            if event.key==pygame.K_RIGHT:
                playerX_change = +5
            if event.key==pygame.K_ESCAPE:
                running = False
            if event.key==pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound=mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX +=playerX_change
    # Taking consideration in size of the spaceship
    if playerX<=0:     playerX=0
    elif playerX>=736: playerX=736

    # Enemy movement for multiple enemies
    for i in range(num_of_enemies):
        # Game_over
        if enemyY[i]>480:
            for j in range(num_of_enemies):
                enemyY[j]=2000 # Move all the enemies out of sight
                playerY = 2000
                bulletY = 2000
            game_over_text()
            break

        enemyX[i] +=enemyX_change[i]
        if enemyX[i]<=0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i]>=736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = is_collision(enemyX[i],enemyY[i],playerX,playerY)
        if collision:
            explosion_sound=mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value +=1
            enemyX[i] = random.randint(0,736)
            enemyY[i] = random.randint(50,150)

        Enemy(enemyX[i],enemyY[i],i)


    # Bullet Movement
    if bulletY<=0:
        bulletY=530
        bullet_state="ready"


    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -=bulletY_change



    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()
