#! /usr/bin/env python3
import pygame, sys, csv, os, eztext
from math import fabs
from time import sleep

# global variables:
screen_x = 640 #screen width
screen_y = 480 #screen height
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
    #highscore vars
highscores = []  
highscore_file = 'highscores.csv'   

# functions:
def read_highscores(filename):
    global highscores
    with open(os.path.join(os.path.dirname(__file__), filename), 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            highscores.append(tuple(row))

def write_highscores(filename):
    global highscores
    with open(os.path.join(os.path.dirname(__file__), filename), 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(highscores)

def gameOver():
    screen.fill(black)
    myFont = pygame.font.SysFont('sans serif', 72)
    GOsurf = myFont.render('GAME OVER', True, white) #2nd arg for AA
    GOrect = GOsurf.get_rect()
    GOrect.midtop = (320, 220)   
    for i, highscore in enumerate(highscores): # checking if there is a new highscore and adding to highscores
        if score>int(highscore[1]):
            txtbx = eztext.Input(x = 20, y = 220,maxlength=45, color=(255,255,255), prompt='NEW HIGHSCORE! Your name: ')
            input_done = False
            name = ''
            while not input_done:
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        name = txtbx.value
                        input_done = True
                        print(name)
                txtbx.update(events)
                screen.fill(black)
                txtbx.draw(screen)
                pygame.display.flip()
            highscores.insert(i, tuple([name, str(score)])) 
            highscores.pop()
            print(highscores)
            break
    # now blitting and drawing everything after getting input
    screen.fill(black)
    screen.blit(GOsurf, GOrect)
    showScore(1)
    pygame.display.flip()
    write_highscores(highscore_file)
    sleep(2)   # wait for 2 secs 
    pygame.quit()   #pygame exit
    sys.exit()  #console exit

def showScore(mode = 0): # mode: 0 means normal corner display, 1 means gameover display with highscores
    global score, screen
    myFont = pygame.font.SysFont('sans serif', 30)
    myFont_small = pygame.font.SysFont('mono', 18)
    if mode == 0:
        myscoreSurf = myFont.render(str(score), True, white)
        myscoreRect = myscoreSurf.get_rect()
        myscoreRect.midtop = (20, 20)
    else:
        myscoreSurf = myFont.render('Your score: '+str(score), True, white)
        myscoreRect = myscoreSurf.get_rect()
        myscoreRect.midtop = (320, 270)
        high_title = myFont.render('High Scores', True, white)
        high_titleRect = high_title.get_rect()
        high_titleRect.midtop = (320, 315)
        screen.blit(high_title, high_titleRect)
        highscore_screens = []
        highscore_rects = []
        score_start_pos = [320, 350]
        for i, highscore in enumerate(highscores):
            highscore_screens.append(myFont_small.render(str(i+1)+'. '+"{:14}".format(highscore[0]) + '{:3}'.format(highscore[1]), True, white))
        for high_screen in highscore_screens:
            highscore_rects.append(high_screen.get_rect())
        for rect in highscore_rects:
            rect.midtop = tuple(score_start_pos)
            score_start_pos[1]+=18
        for high_screen, rect in zip(highscore_screens, highscore_rects):
            screen.blit(high_screen, rect)
    screen.blit(myscoreSurf, myscoreRect)

def pauseScreen():
    global screen
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
            if event.key == pygame.K_SPACE:
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
        ball['x'] += 2*ball['x_speed']/fabs(ball['x_speed'])
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

# initializations:
pygame.init()
pygame.display.set_caption('Squash')
screen = pygame.display.set_mode((screen_x, screen_y))
clock = pygame.time.Clock()
read_highscores(highscore_file)

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