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
gold = (239, 229, 51)
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

def blit_text(screen, text, midtop, aa=True, font=None, font_name = None, size = None, color=(255,0,0)):
    if font is None:                                    # font option is provided to save memory if font is
        font = pygame.font.SysFont(font_name, size)     # already loaded and needs to reused many times
    font_surface = font.render(text, aa, color)
    font_rect = font_surface.get_rect()
    font_rect.midtop = midtop
    screen.blit(font_surface, font_rect)

def gameOver():
    global screen, score
    for i, highscore in enumerate(highscores): # checking if there is a new highscore and adding to highscores
        if score>int(highscore[1]):
            txtbx = eztext.Input(x = 150, y = 240,maxlength=45, color=(255,255,255), prompt='Your name: ')
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
                blit_text(screen, 'NEW HIGHSCORE!', (320, 180), font_name='sans serif', size=50, color=gold, )
                txtbx.draw(screen)
                pygame.display.flip()
            highscores.insert(i, tuple([name, str(score)])) 
            highscores.pop()
            print(highscores)
            break
    # now blitting and drawing everything after getting input
    screen.fill(black)
    blit_text(screen, 'GAME OVER', (320, 200), font_name='sans serif', size=72, color=white)
    showScore(1)
    pygame.display.flip()
    write_highscores(highscore_file)
    sleep(2)   # wait for 2 secs 
    pygame.quit()   #pygame exit
    sys.exit()  #console exit

def showScore(mode = 0): # mode: 0 means normal corner display, 1 means gameover display with highscores
    global score, screen
    sans_font = pygame.font.SysFont('sans serif', 30)
    mono_font = pygame.font.SysFont('mono', 18)
    if mode == 0:
        blit_text(screen, str(score), (20,20), font=sans_font, color=white)
    else:
        blit_text(screen, 'Your score: '+str(score), (320, 270), font=sans_font, color=white)
        blit_text(screen, 'High Scores', (320, 315), font_name='sans serif', size=25, color=white)
        #blit_text(screen, '---------------------', (320, 327), font_name='sans serif',  size=25, color=white)
        score_start_pos = [320, 350]
        for i, highscore in enumerate(highscores):
            blit_text(screen, str(i+1)+'. '+"{:14}".format(highscore[0])+'{:3}'.format(highscore[1]),
                      tuple(score_start_pos), font = mono_font, color = white  )
            score_start_pos[1]+=18

def pauseScreen():
    global screen
    translucentBkg = pygame.Surface((screen_x, screen_y), pygame.SRCALPHA)
    translucentBkg.fill((50, 50, 50, 100))
    screen.blit(translucentBkg, (0, 0))
    blit_text(screen, 'Paused', (320, 240), font_name='sans serif', size=50, color=white)

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