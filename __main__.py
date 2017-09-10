#! /usr/bin/env python3
import pygame

# global variables:
screen_x = 640
screen_y = 480
paddle = {
    'width': 70,
    'height': 10,
    'x': screen_x/2 - 35,
    'y': screen_y - 10,
    'speed': 2
}
ball = {
    'size': 10,
    'x': screen_x/2 - 5,
    'y': screen_y/2 - 5,
    'x_speed': 0,
    'y_speed': 4
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

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_LEFT]:
        paddle['x'] -= paddle['speed']
    if pressed[pygame.K_RIGHT]:
        paddle['x'] += paddle['speed']
    
    # drawing everything:
    screen.fill(black)
    pygame.draw.rect(screen, white, pygame.Rect(paddle['x'], paddle['y'], paddle['width'], paddle['height']))
    pygame.draw.rect(screen, white, pygame.Rect(ball['x'], ball['y'], ball['size'], ball['size']))
    pygame.display.flip()
    clock.tick()