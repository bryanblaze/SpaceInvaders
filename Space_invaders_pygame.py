import pygame
import random
import math
from pygame import mixer
#initialize pygame
pygame.init()
# Create Screen
screen=pygame.display.set_mode((800,600))
#score
score_value=0
font=pygame.font.Font('freesansbold.ttf',32)
textX=10
textY=10
#Game over text
over_font=pygame.font.Font('freesansbold.ttf',64)
#Background Music
mixer.music.load('background.wav')
mixer.music.play(-1)
#Background
background=pygame.image.load("bg.png")
#Title and Icon
pygame.display.set_caption("Space Invaders")
icon=pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)
#Player
playerimg=pygame.image.load('player.png')
playerX=370
playerY=480
playerX_change=0
#Enemy
enemyimg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
no_of_enemies=6
for i in range(no_of_enemies):
    enemyimg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,735))  #gives random coordinates from 0to800
    enemyY.append(random.randint(50,150))
    enemyX_change.append(4)
    enemyY_change.append(40)
#Bullet
bulletimg=pygame.image.load('bullet.png')
bulletX=0  #gives random coordinates from 0to800
bulletY=480
bulletX_change=0
bulletY_change=10
bullet_state="ready"  #READY MEANS YOU CANT SEE BULLET IN SCREEN(MOVEMENT OF BULLET)



def player(x,y):
    screen.blit(playerimg,(x,y)) #blit means to draw(draw player on screen)

def enemy(x,y,i):
    screen.blit(enemyimg[i],(x,y))
def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletimg,(x+5,y+10)) #x+16 and y+10 is for bullet coming out of middle of spacship
def Collision(enemyX,enemyY,bulletX,bulletY):
    dist=math.sqrt((math.pow(enemyX-bulletX,2))+(math.pow(enemyY-bulletY,2))) #distance formula
    if dist < 27:
        return True
    else:
        return False
def show_score(x,y):
    score=font.render("Score :"+str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))
def game_over():
    over_text=over_font.render('GAME OVER !!',True,(255,255,255))
    screen.blit(over_text,(200,250))     



#Game loop
running=True
while running:
    #rgb color code for background 
    screen.fill((0,0,0)) 
    #background
    screen.blit(background,(0,0))
    for event in pygame.event.get():  #gets all of events happening
        if event.type==pygame.QUIT:  #checks if close button ispressed and exits the loop
                                    running=False                 
     # if keystroke is pressed check if it  is right or left
        if event.type==pygame.KEYDOWN:
                                    if event.key==pygame.K_LEFT:#K left is left arrow key,check if it is pressed 
                                        playerX_change=-8
       
                                    if event.key==pygame.K_RIGHT:#K right is right arrow key 
                                        playerX_change=8                          
        
                                    
                                    if event.key==pygame.K_RIGHT:#K right is right arrow key 
                                        playerX_change=8 
                                        
                                    if event.key==pygame.K_SPACE:# if space is pressed
                                        if bullet_state is "ready":
                                            bullet_sound=mixer.Sound('laser.wav')
                                            bullet_sound.play()
                                            bulletX=playerX
                                            fire_bullet(bulletX,bulletY)

                                
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_RIGHT or event.key==pygame.K_LEFT: #check if key is released
                 playerX_change=0
             
             
    playerX+=playerX_change    
    #assign border so spaceship doesnt leave the screen
    if playerX <= 0: 
        playerX=0
    elif playerX >= 736:
        playerX=736
    
        
    #enemy movement
    for i in range(no_of_enemies):
        
        #gameover
        if enemyY[i] >440:
            for j in range(no_of_enemies):
                enemyY[j]=2000
            game_over()
            break
        
        
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0: 
            enemyX_change[i]=6
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i]=-6
            enemyX[i] += enemyX_change[i]
            enemyY[i] += enemyY_change[i]
        #Collision
        collision=Collision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explosion=mixer.Sound('explosion.wav')
            explosion.play()
            bulletY=480
            bullet_state="ready"
            score_value +=1
            #respawning enemy
            enemyX[i]=random.randint(0,735)  #gives random coordinates from 0to800
            enemyY[i]=random.randint(50,150) 
            #coordinates of enemy updated
        enemy(enemyX[i],enemyY[i],i)           
    #bullet movement
    if bulletY <=0:
        bulletY=480
        bullet_state="ready"
    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY-=bulletY_change
    
        
    #coordinates of player  updated    
    player(playerX,playerY)
    show_score(textX,textY)
    #update display
    pygame.display.update()
    