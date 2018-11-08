
from Ball import Ball
from Brick import Brick
from GameObject import GameObject

import pygame
import sys
import os
import math

game = GameObject()

# game.bricks_x, game.bricks_y = 7, 11
# game.brick_size = 60
# SCREEN_WIDTH = game.bricks_x * BRICK_SIZE
# SCREEN_HIGHT = game.bricks_y * BRICK_SIZE
# DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HIGHT))
# INIT_POSITION = (SCREEN_WIDTH//2, 10*BRICK_SIZE)

FPS = 60
FPS_CLOCK = pygame.time.Clock()

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

pygame.init()
pygame.display.set_caption('B-Breaker!')


def main():
    # game.show(bricks, balls)
    # game.update(DISPLAYSURF, balls, bricks)
    balls = pygame.sprite.Group()
    bricks = pygame.sprite.Group()
    ball_rect = pygame.Rect(330, 380, 40, 40)

    start_pos = [-1, -1]  # just to initialize?
    end_pos = [-1, -1]

    balls_count = 0
    while True:
        # print(game.if_next_level)
        if not game.game_on and game.next_level:
            game.generate_next_level(balls, bricks)
            # print(game.if_next_level)

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

            if event.type == pygame.MOUSEBUTTONUP and not game.game_on:
                if pygame.mouse.get_pressed()[0] == 0 and start_pos != [-1,-1]:
                    end_pos = event.pos
                    if end_pos[1] > start_pos[1]:
                        for ball in balls:
                            ball.calculateVelocity(start_pos, end_pos)
                            # ball.game_on = True
                        # game_on = True
                        game.game_on = True
                        game.next_level = True
                        pygame.time.set_timer(Ball.timer, 150)
                        balls.sprites()[0].game_on = True
                        # ball timer ilość i czas uzależniony od len(balls)
                        # timer_ball on
                        # set first ball.game_on = True
                start_pos = [-1, -1]
            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0] == 1:
                    intermediate_pos = event.pos
                    # print(intermediate_pos)
                if ball_rect.collidepoint(event.pos):
                    pygame.mouse.set_cursor(*pygame.cursors.diamond)
                else:
                    pygame.mouse.set_cursor(*pygame.cursors.arrow)



            if event.type == Ball.timer:
                
                balls_count += 1
                # print("Ball.timer! balls_count = ", balls_count)
                if balls_count < len(balls):
                    balls.sprites()[balls_count].game_on = True
                    # print("True")
                else:
                    pygame.time.set_timer(Ball.timer, 0)
                    # print("False")
                    balls_count = 0

        game.update(balls, bricks)
        FPS_CLOCK.tick(FPS)




if __name__ == "__main__":
    main()


# x1, y1 = position
# x2, y2 = self.circle.center
# distance = math.hypot(x1 - x2, y1 - y2)

# pygame.mouse.set_cursor(*pygame.cursors.sizer_x_strings)
# *pygame.cursors.broken_x - złapanie do celowania
# *pygame.cursors.tri_left - ładny do przycisków i ogólnie

# os.environ['SDL_VIDEO_CENTERED'] = '1'

# r1 = pygame.draw.rect(DISPLAYSURF, WHITE, (100, 100, 50, 50))
# r2 = pygame.draw.rect(DISPLAYSURF, (255, 255, 0), (200, 200, 50, 50), 5)
# if r1.collidepoint(event.pos):
#     pygame.draw.rect(DISPLAYSURF, (0, 255, 0), r1)
# if r2.collidepoint(event.pos):
#     # pygame.draw.rect(DISPLAYSURF, red, r2)
#     pygame.draw.rect(DISPLAYSURF, (255, 0, 0), (200, 200, 50, 50), 20)