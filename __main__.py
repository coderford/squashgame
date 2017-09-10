#! /usr/bin/env python3
import pygame, time, sys

# global variables:
screen_x = 640
screen_y = 480
paddle = {
    'width': 70,
    'height': 10,
    'x': screen_x/2 - 35,
    'y': screen_y - 10,
    'speed': 10
}
ball = {
    'size': 10,
    'x': screen_x/2 - 5,
    'y': screen_y/2 - 5,
    'x_speed': 5,
    'y_speed': -10
}
framerate = 60
score = 0
done = False
    # some colors:
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)    

# initializations:
pygame.init()
pygame.display.set_caption('Squash')
screen = pygame.display.set_mode((screen_x, screen_y))
clock = pygame.time.Clock()

def gameOver():
    screen.fill(black)
    myFont = pygame.font.SysFont('sans serif', 72)
    GOsurf = myFont.render('GAME OVER', True, white) #2nd arg for AA
    GOrect = GOsurf.get_rect()
    GOrect.midtop = (320, 220)   
    screen.blit(GOsurf, GOrect)
    showScore(1)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()   #pygame exit
    sys.exit()  #console exit

def showScore(mode = 0):
    myFont = pygame.font.SysFont('sans serif', 30)
    if mode == 0:
        scoreSurf = myFont.render(str(score), True, white)
        scoreRect = scoreSurf.get_rect()
        scoreRect.midtop = (20, 20)
    else:
        scoreSurf = myFont.render('Your score: '+str(score), True, white)
        scoreRect = scoreSurf.get_rect()
        scoreRect.midtop = (320, 300)
    screen.blit(scoreSurf, scoreRect)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
    # paddle movement:
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_LEFT]:
        paddle['x'] -= paddle['speed']
    if pressed[pygame.K_RIGHT]:
        paddle['x'] += paddle['speed']

    # ball collisions:
        # walls:
    if ball['x']+ball['size'] > screen_x or ball['x'] < 0:
        ball['x_speed'] = -ball['x_speed']
    if ball['y'] < 0:
        ball['y_speed'] = -ball['y_speed']
        # paddle:
    if paddle['x']-ball['size']<=ball['x']<=paddle['x']+paddle['width']:
        if ball['y_speed'] > 0:
            if ball['y'] + ball['size'] >= paddle['y']:
                ball['y_speed'] = -ball['y_speed']
                score += 1

    # game over detection:
    if ball['y'] > paddle['y'] and ball['y_speed'] > 0:
        gameOver()
    # ball movement:
    ball['x'] += ball['x_speed']
    ball['y'] += ball['y_speed']
    # drawing everything:
    screen.fill(black)
    pygame.draw.rect(screen, white, pygame.Rect(paddle['x'], paddle['y'], paddle['width'], paddle['height']))
    pygame.draw.rect(screen, white, pygame.Rect(ball['x'], ball['y'], ball['size'], ball['size']))
    showScore()
    pygame.display.flip()
    clock.tick(framerate)