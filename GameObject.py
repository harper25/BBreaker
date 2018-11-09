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
        self.next_level = True
        self.shot_counter = 0
        self.ball_timer = pygame.USEREVENT + 1
        self.level = 0

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

        if {ball.game_on for ball in balls} == {False}:
            self.game_on = False

    def generate_next_level(self, balls, bricks):
        print("GENERATE!!!!!!!!!!!!!!!!!!!!!!!")

        br1 = Brick(pygame.Rect(self.brick_size, self.brick_size, self.brick_size, self.brick_size), number=12, color=(30, 240, 20))
        # br1.draw(self.surface)

        br2 = Brick(pygame.Rect(3*self.brick_size, 2*self.brick_size, self.brick_size, self.brick_size), number=34, color=(200, 60, 80))
        # br2.draw(self.surface)
        bricks.add(br1, br2)

        new_ball = Ball(self.surface, 350, 400, 10, 10)
        balls.add(new_ball)

        print('LENGTH BALLS: ', len(balls))

        # self._update(balls, bricks)
        self.next_level = False

    def handle_shots(self, balls):
        self.shot_counter += 1
        if self.shot_counter < len(balls):
            balls.sprites()[self.shot_counter].game_on = True
        else:
            pygame.time.set_timer(self.ball_timer, 0)
            self.shot_counter = 0
