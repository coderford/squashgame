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
paused = False
    # some colors:
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)    

# initializations:
pygame.init()
pygame.display.set_caption('Squash')
screen = pygame.display.set_mode((screen_x, screen_y))
clock = pygame.time.Clock()

# functions:
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

def pauseScreen():
    translucentBkg = pygame.Surface((screen_x, screen_y), pygame.SRCALPHA)
    translucentBkg.fill((50, 50, 50, 100))
    myFont = pygame.font.SysFont('sans serif', 50)
    pauseSurf = myFont.render('Paused', True, white)
    pauseRect = pauseSurf.get_rect()
    pauseRect.midtop = (screen_x/2, screen_y/2)
    screen.blit(translucentBkg, (0, 0))
    screen.blit(pauseSurf, pauseRect)

def handle_events():
    global paused, done
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            if event.key == pygame.K_RETURN:
                paused = not paused

def paddle_updates():
    # paddle movement:
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_LEFT] and paddle['x']>=0:
        paddle['x'] -= paddle['speed']
    if pressed[pygame.K_RIGHT] and paddle['x']<=screen_x-paddle['width']:
        paddle['x'] += paddle['speed']
    # paddle collisions:
    if paddle['x'] + paddle['width'] >= screen_x:
        paddle['x'] = screen_x - paddle['width']
    if paddle['x'] <= 0:
        paddle['x'] = 0

def ball_updates():
    global score
    # ball collisions:
        # with walls:
    if ball['x']+ball['size'] > screen_x or ball['x'] < 0:
        ball['x_speed'] = -ball['x_speed']
    if ball['y'] < 0:
        ball['y_speed'] = -ball['y_speed']
        # with paddle:
    if paddle['x']-ball['size']<=ball['x']<=paddle['x']+paddle['width']:
        if ball['y_speed'] > 0:
            if ball['y'] + ball['size'] >= paddle['y']:
                ball['y_speed'] = -ball['y_speed']
                ball['x_speed'] = (ball['x']+5 - (paddle['x']+paddle['width']/2))/(paddle['width']/2)*10
                score += 1
    # ball movement:
    ball['x'] += ball['x_speed']
    ball['y'] += ball['y_speed']

def draw():
    screen.fill(black)
    pygame.draw.rect(screen, white, pygame.Rect(paddle['x'], paddle['y'], paddle['width'], paddle['height']))
    pygame.draw.rect(screen, white, pygame.Rect(ball['x'], ball['y'], ball['size'], ball['size']))
    showScore()
    if paused:
        pauseScreen()
    pygame.display.flip()
    clock.tick(framerate)

# main loop:
while not done:
    handle_events()
    if not paused:
        paddle_updates()
        ball_updates()
        # game over detection:
        if ball['y'] > paddle['y'] and ball['y_speed'] > 0:
            gameOver()
    draw()