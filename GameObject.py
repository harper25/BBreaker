import pygame
from Ball import Ball
from Brick import Brick


class GameObject():

    def __init__(self, bricks_x=7, bricks_y=11, brick_size=60):
        print('Game!')
        self.bricks_x = bricks_x
        self.bricks_y = bricks_y
        self.brick_size = brick_size
        self.screen_width = self.brick_size * self.bricks_x
        self.screen_height = self.brick_size * self.bricks_y
        self.surface = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.init_position = (2*self.screen_width//2, 10*self.brick_size)
        self.game_on = False
        self.if_next_level = True

    @staticmethod
    def show(balls, bricks):
        print(balls, ' ', bricks)

    def update(self, balls, bricks):
        # if self.game_on:  # nie wchodzi!
        self._update(balls, bricks)

    def _update(self, balls, bricks):
        color = (10, 50, 30)
        self.surface.fill(color)
        balls.update(self.surface)
        bricks.update(self.surface)
        pygame.display.update()

        ball_game_on = {ball.game_on for ball in balls}

        print(ball_game_on)
        if len(ball_game_on) == 1 and not ball_game_on:  # ?
            self.game_on = False
            self.generate_next_level = True

    def generate_next_level(self, balls, bricks):
        print("GENERATE!!!!!!!!!!!!!!!!!!!!!!!")

        br1 = Brick(pygame.Rect(self.brick_size, self.brick_size, self.brick_size, self.brick_size), number=12, color=(30, 240, 20))
        br1.draw(self.surface)

        br2 = Brick(pygame.Rect(3*self.brick_size, 2*self.brick_size, self.brick_size, self.brick_size), number=34, color=(200, 60, 80))
        br2.draw(self.surface)

        ball_speed = 10
        ball1 = Ball(self.surface, 350, 400, ball_speed, 10)
        ball2 = Ball(self.surface, 350, 400, ball_speed, 10)
        ball3 = Ball(self.surface, 350, 400, ball_speed, 10)

        balls.add(ball1, ball2, ball3)
        bricks.add(br1, br2)

        new_ball = Ball(self.surface, 350, 400, 10, 10)
        balls.add(new_ball)

        print('LENGTH BALLS: ', len(balls))

        self._update(balls, bricks)
        self.if_next_level = False
