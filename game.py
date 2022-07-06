
import sys, pygame
import os
pygame.font.init()


pygame.init()
WIDTH,HEIGHT = 900,500
pygame.display.set_caption("Game of four")
WIN = pygame.display.set_mode((WIDTH,HEIGHT))


HEALTH_FONT = pygame.font.SysFont('comicsans',40)
WINNER_FONT = pygame.font.SysFont('comicsans',100)
FPS = 60
VEL=5
BULLENT_VEL = 7
MAX_BULLETS = 3

CHAR_WID = 100
CHAR_HEI = 100
CHAR_DIMENSION = (CHAR_WID,CHAR_HEI)
BORDER = pygame.Rect(WIDTH//2-5,0,10,HEIGHT)

WHITE=(255,255,255)
BLACK=(0,0,0)
RED  = (255,0,0)
YELLOW = (255,255,0)

NARUTO_IMAGE = pygame.image.load(os.path.join('Assets','naruto.gif'))
NARUTO_IMG  = pygame.transform.scale(NARUTO_IMAGE,CHAR_DIMENSION)
SASUKE_IMAGE = pygame.image.load(os.path.join('Assets','sasuke.gif'))
SASUKE_IMG  = pygame.transform.scale(SASUKE_IMAGE,CHAR_DIMENSION)

NARUTO_HIT = pygame.USEREVENT+1
SASUKE_HIT = pygame.USEREVENT+2

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets','bg.jpg')),(WIDTH,HEIGHT))

def naruto_movement(keys_pressed ,naruto):
    if keys_pressed[pygame.K_a] and naruto.x > 0 : #LEFT
            naruto.x -= VEL
    if  keys_pressed[pygame.K_d] and naruto.x  + CHAR_WID < BORDER.x: #RIGHT
            naruto.x += VEL
    if  keys_pressed[pygame.K_w] and naruto.y> 0 : #UP
            naruto.y -= VEL
    if  keys_pressed[pygame.K_s] and naruto.y + CHAR_HEI < HEIGHT: #DOWN
            naruto.y += VEL

def sasuke_movement(keys_pressed ,sasuke):
    if keys_pressed[pygame.K_LEFT] and sasuke.x > BORDER.x: #LEFT
            sasuke.x -= VEL
    if  keys_pressed[pygame.K_RIGHT] and sasuke.x < WIDTH-CHAR_WID: #RIGHT
            sasuke.x += VEL
    if  keys_pressed[pygame.K_UP] and sasuke.y > 0: #UP
            sasuke.y -= VEL
    if  keys_pressed[pygame.K_DOWN] and sasuke.y + CHAR_HEI < HEIGHT: #DOWN
            sasuke.y += VEL


def draw_widow(naruto,sasuke,naruto_bullets,sasuke_bullets,nartuo_hel,sasuke_hel):
    WIN.blit(SPACE,(0,0))
    n_health_text = HEALTH_FONT.render('Health:'+str(nartuo_hel),1,WHITE)
    s_health_text = HEALTH_FONT.render('Health:'+str(sasuke_hel),1,WHITE)
    WIN.blit(n_health_text,(WIDTH-n_health_text.get_width(),10))
    WIN.blit(s_health_text,(10,10))
    pygame.draw.rect(WIN,BLACK,BORDER)
    WIN.blit(NARUTO_IMG,(naruto.x,naruto.y))
    WIN.blit(SASUKE_IMG,(sasuke.x,sasuke.y))

    for bullet in naruto_bullets:
        pygame.draw.rect(WIN,RED,bullet)

    for bullet in sasuke_bullets:
        pygame.draw.rect(WIN,YELLOW,bullet)
    pygame.display.update()

def handle_bullets(naruto_bullets,sasuke_bullets,naruto,sasuke):
        for bullet in naruto_bullets:
                bullet.x += BULLENT_VEL
                if sasuke.colliderect(bullet):
                        pygame.event.post(pygame.event.Event(NARUTO_HIT))
                        naruto_bullets.remove(bullet)   
                elif bullet.x > WIDTH:
                        naruto_bullets.remove(bullet)
        for bullet in sasuke_bullets:
                bullet.x -=  BULLENT_VEL
                if naruto.colliderect(bullet):
                        pygame.event.post(pygame.event.Event(SASUKE_HIT))
                        sasuke_bullets.remove(bullet) 
                elif bullet.x < 0:
                        sasuke_bullets.remove(bullet)
def main():

    naruto  = pygame.Rect(0,10,CHAR_WID,CHAR_HEI)
    sasuke = pygame.Rect(800,10,CHAR_WID,CHAR_HEI)
    naruto_hel = 10 
    sasuke_hel= 10

    naruto_bullets = []
    sasuke_bullets = []
    clock = pygame.time.Clock() 
    run = True
    while(run):
        clock.tick(FPS)  #Set FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN and len(naruto_bullets) < MAX_BULLETS:
                if event.key == pygame.K_LCTRL:
                        bullet = pygame.Rect(naruto.x + naruto.width , naruto.y+(naruto.height//2)-2,10,5)
                        naruto_bullets.append(bullet)               
                if event.key == pygame.K_RCTRL and len(sasuke_bullets) < MAX_BULLETS:
                        bullet = pygame.Rect(sasuke.x , sasuke.y+sasuke.height//2-2,10,5)
                        sasuke_bullets.append(bullet)    
            if event.type == NARUTO_HIT:
                naruto_hel-=1
            if event.type == SASUKE_HIT:
                sasuke_hel-=1
        winner_text = ''
        if naruto_hel <= 0 :
                winner_text = "naruto wins"
        if sasuke_hel <= 0 :
                winner_text = "sasuke wins"

        if winner_text != '':
                draw_winner(winner_text)
                break


        keys_pressed = pygame.key.get_pressed()
        naruto_movement(keys_pressed , naruto)
        sasuke_movement(keys_pressed,sasuke)
        handle_bullets(naruto_bullets,sasuke_bullets,naruto,sasuke)
        draw_widow(naruto,sasuke,naruto_bullets,sasuke_bullets,naruto_hel,sasuke_hel)


    main()

def draw_winner(text):
        draw_text = WINNER_FONT.render(text,1,RED)
        WIN.blit(draw_text,(WIDTH//2-draw_text.get_width()//2  , HEIGHT//2))
        pygame.display.update()
        pygame.time.delay(5000)

if __name__ == "__main__":
    main()

