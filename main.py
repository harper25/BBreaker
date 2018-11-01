
from Ball import Ball
from Brick import Brick
from Game import Game

import pygame
import sys
import os
# from pygame.locals import *
import math


# gems = pygame.sprite.Group()
# gems.add(gem)
# gems = pygame.sprite.Group(gem1, gem2)

X = 7
Y = 11
BRICK_SIZE = 60

# x1, y1 = position
# x2, y2 = self.circle.center
# distance = math.hypot(x1 - x2, y1 - y2)

# RGB
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
# screen_width = 600
# screen_height = 500
screen_width = X * BRICK_SIZE
screen_height = Y * BRICK_SIZE


pygame.init()
FPS = 60  # Frames Per Second
fpsClock = pygame.time.Clock()


# pygame.mouse.set_cursor(*pygame.cursors.sizer_x_strings)
# *pygame.cursors.broken_x - złapanie do celowania
# *pygame.cursors.tri_left - ładny do przycisków i ogólnie


print(pygame.USEREVENT)
ballTimer = pygame.USEREVENT + 1

game_on = False

# os.environ['SDL_VIDEO_CENTERED'] = '1'
DISPLAYSURF = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption('B-Breaker!')

# x, y (lewy górny róg), szerokość, wysokość
r1 = pygame.draw.rect(DISPLAYSURF, WHITE, (100, 100, 50, 50))

r2 = pygame.draw.rect(DISPLAYSURF, (255, 255, 0), (200, 200, 50, 50), 5)

br1 = Brick(rect=pygame.Rect(BRICK_SIZE,BRICK_SIZE,BRICK_SIZE,BRICK_SIZE), number=12, color=(30, 240, 20))
br1.draw(DISPLAYSURF)

br2 = Brick(rect=pygame.Rect(3*BRICK_SIZE,2*BRICK_SIZE,BRICK_SIZE,BRICK_SIZE), number=34, color=(200, 60, 80))
br2.draw(DISPLAYSURF)

ball_speed = 10

ball1 = Ball(surface = DISPLAYSURF, x=350, y=400, speed = ball_speed, size=10)

ball_rect = pygame.Rect(330, 380, 40, 40)

ball2 = Ball(surface = DISPLAYSURF, x=350, y=400, speed = ball_speed, size=10)

ball3 = Ball(surface = DISPLAYSURF, x=350, y=400, speed = ball_speed, size=10)

balls = [ball1, ball2, ball3]
balls.append(Ball(surface = DISPLAYSURF, x=350, y=400, speed = ball_speed, size=10))
print(balls[0])
balls_count = len(balls)
print("Length balls: ", balls_count)



start_pos = [-1, -1] # just to initialize?
end_pos = [-1, -1]


def main():
    balls_count = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                print('Clicked!')
                mouseButtons = pygame.mouse.get_pressed()
                if mouseButtons[0] == 1:
                    # mousePosition = pygame.mouse.get_pos()
                    print(event.pos)
                    start_pos = event.pos
                    if r1.collidepoint(event.pos):
                        pygame.draw.rect(DISPLAYSURF, (0, 255, 0), r1)
                    if r2.collidepoint(event.pos):
                        # pygame.draw.rect(DISPLAYSURF, red, r2)
                        pygame.draw.rect(DISPLAYSURF, (255, 0, 0), (200, 200, 50, 50), 20)
            if event.type == pygame.MOUSEBUTTONUP:
                if pygame.mouse.get_pressed()[0] == 0 and start_pos != [-1,-1]:
                    end_pos = event.pos
                    if end_pos[1] > start_pos[1]:
                        for ball in balls:
                            ball.calculateVelocity(start_pos, end_pos)
                            # ball.game_on = True
                        # game_on = True
                        pygame.time.set_timer(ballTimer, 150)
                        balls[0].game_on = True
                        # ball timer ilość i czas uzależniony od len(balls)
                        # timer_ball on
                        # set first ball.game_on = True
                start_pos = [-1, -1]
            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0] == 1:
                    intermediate_pos = event.pos
                    print(intermediate_pos)
                if ball_rect.collidepoint(event.pos):
                    pygame.mouse.set_cursor(*pygame.cursors.diamond)
                else:
                    pygame.mouse.set_cursor(*pygame.cursors.arrow)



            if event.type == ballTimer:
                
                balls_count += 1
                print("ballTimer! balls_count = ", balls_count)
                if balls_count < len(balls):
                    balls[balls_count].game_on = True
                    print("True")
                else:
                    pygame.time.set_timer(ballTimer, 0)
                    print("False")
                    balls_count = 0
                    #zmienna globalna manager game_on

        
        for ball in balls:
            if ball.game_on:
                ball.update(DISPLAYSURF)

        pygame.display.update()
        fpsClock.tick(FPS)




if __name__ == "__main__":
    main()