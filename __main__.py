#! /usr/bin/env python3
import pygame, sys, csv, os, eztext
from math import fabs
from time import sleep

# Ball class
class Ball():
    def __init__(self, screen, size=None, x=None, y=None, x_speed=None, y_speed=None):
        if size is None:
            self.size = 10
            self.x = screen_x/2-self.size/2
            self.y = screen_y/2
            self.x_speed = 5
            self.y_speed = -10
        else:
            self.size = size
            self.x = x
            self.y = y
            self.x_speed = x_speed
            self.y_speed = y_speed

    def draw(self, screen):
        pygame.draw.rect(screen, white, pygame.Rect(self.x, self.y, self.size, self.size))
        return
    def wall_collisions(self, screen):
        return_val = False
        screen_x = screen.get_width()
        screen_y = screen.get_height()
        if self.x+self.size > screen_x or self.x < 0:
            self.x_speed = -self.x_speed
            self.x += 2*self.x_speed/fabs(self.x_speed)
            return_val = True
        if self.y < 0:
            self.y_speed = -self.y_speed
            return_val = True
        return return_val
    def paddle_collisions(self, paddle):
        if paddle.x-self.size<=self.x<=paddle.x+paddle.width:
            if self.y_speed > 0:
                if self.y + self.size >= paddle.y:
                    self.y_speed = -self.y_speed
                    self.x_speed = (self.x+5 - (paddle.x+paddle.width/2))/(paddle.width/2)*10
                    return True
        return False
    def handle_movement(self):
        self.x += self.x_speed
        self.y += self.y_speed 
# Paddle class
class Paddle():
    def __init__(self, screen):
        self.width = 70
        self.height = 10
        self.x = screen.get_width()/2 - self.width/2
        self.y = screen.get_height() - self.height
        self.speed = 10
    def draw(self, screen):
        pygame.draw.rect(screen, white, pygame.Rect(self.x, self.y, self.width, self.height))
        return
    def wall_collisions(self, screen):
        if self.x + self.width >= screen.get_width():
            self.x = screen.get_width() - self.width
        if self.x <= 0:
            self.x = 0
        return
    def handle_movement(self, screen):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT] and self.x>=0:
            self.x -= self.speed
        if pressed[pygame.K_RIGHT] and self.x<=screen.get_width()-self.width:
            self.x +=self.speed
        return

# global variables:
screen_x = 640 #screen width
screen_y = 480 #screen height
framerate = 60
score = 0
done = False
paused = False
    # some colors:
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
gold = (239, 229, 51)
blue = (78,162,196)
    # highscore vars
highscores = []  
highscore_file = 'highscores.csv'  
sounds = {} 

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

def menu_screen():  # to be called before starting actual game loop
    global screen
    menu_done = False
    menuitems = ['Play', 'Quit'] 
    focus_index = 0
    # bkg balls initialization
    balls = []
    count = 20
    for i in range(count):
        balls.append(Ball(screen, 10, screen.get_width()/2-5, i*screen.get_height()/count, (-1)**i*10*(fabs(count/2-i)+1), 0))
    # -------
    while not menu_done:  # every screen/scene/level has its own loop
        screen.fill(black)
        # bkg balls drawing
        for ball in balls:
            ball.wall_collisions(screen)
            ball.handle_movement()
            ball.draw(screen)
        translucentBkg = pygame.Surface((screen_x, screen_y), pygame.SRCALPHA)
        translucentBkg.fill((50, 50, 50, 200))
        screen.blit(translucentBkg, (0, 0))
        #------------
        blit_text(screen, 'Squash', (320,180), font_name='sans serif', size=70, color=gold)
        menu_ypos = 260
        for i, menuitem in enumerate(menuitems):
            textcolor = white
            if focus_index == i:
                textcolor = blue
            blit_text(screen,menuitem, (320, menu_ypos), font_name='sans serif', size=35, color=textcolor)
            menu_ypos += 30
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    focus_index -= 1
                if event.key == pygame.K_DOWN:
                    focus_index += 1
                if event.key == pygame.K_RETURN:
                    menu_done = True
        if focus_index==len(menuitems): focus_index = 0
        elif focus_index<0: focus_index = len(menuitems)-1
        clock.tick(60)
    if focus_index == 1:
        pygame.quit()
        sys.exit()


def gameOver(): # game over screen
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
            clock.tick(60)
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

def pause_screen():
    global screen
    translucentBkg = pygame.Surface((screen_x, screen_y), pygame.SRCALPHA)
    translucentBkg.fill((50, 50, 50, 100))
    screen.blit(translucentBkg, (0, 0))
    blit_text(screen, 'Paused', (320, 240), font_name='sans serif', size=50, color=white)
    pygame.display.flip()

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

def draw():
    screen.fill(black)
    paddle.draw(screen)
    ball.draw(screen)
    showScore()
    

# initializations:
# these two mixer initializations seem to be necessary to avoid delaying of sounds
pygame.mixer.pre_init(44100, -16, 2, 512)  # sets a larger buffer size?
pygame.mixer.init()
pygame.init()
pygame.display.set_caption('Squash')
screen = pygame.display.set_mode((screen_x, screen_y))
clock = pygame.time.Clock()
read_highscores(highscore_file)
# initializing ball and paddle:
paddle = Paddle(screen)
ball = Ball(screen)
#initializing sounds:
sounds['hit_paddle'] = pygame.mixer.Sound('sfx/sounds/hit_paddle.wav')
sounds['hit_wall'] = pygame.mixer.Sound('sfx/sounds/hit_wall.wav')
for sound in sounds.values():
    sound.set_volume(20)

menu_screen()

# main loop:
while not done:
    handle_events()
    if not paused:
        paddle.wall_collisions(screen)
        paddle.handle_movement(screen)  
        if ball.wall_collisions(screen):
            sounds['hit_wall'].play()
        if ball.paddle_collisions(paddle):
            sounds['hit_paddle'].play()
            score += 1
        ball.handle_movement()
        # game over detection:
        if ball.y > paddle.y and ball.y_speed> 0:
            gameOver()
    draw()
    if paused:
        pause_screen()
    clock.tick(framerate)
    pygame.display.flip()