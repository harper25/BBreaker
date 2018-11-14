import random
import pygame
from Ball import Ball
from Brick import Brick


class GameObject():

    def __init__(self, bricks_x=7, bricks_y=11, brick_size=60):
        print('Game!')
        random.seed()
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
        color = (10, 50, 30)
        self.surface.fill(color)
        balls.update(self.surface)
        bricks.update(self.surface)
        pygame.display.update()

        if {ball.game_on for ball in balls} == {False}:
            self.game_on = False

    def generate_next_level(self, balls, bricks):
        print("GENERATE!!!!!!!!!!!!!!!!!!!!!!!")


        self.level += 1

        # add new bricks
        new_bricks_count = random.randint(1, self.bricks_x-2)
        positions_x = random.sample(range(0, self.bricks_x), new_bricks_count)
        # create rect inside Brick class in init, pass brick
        for i in range(new_bricks_count):
            bricks.add(Brick(pygame.Rect(positions_x[i]*self.brick_size, 0, self.brick_size, self.brick_size), number=self.level, color=(30, 240, 20)))
        # move bricks down

        # not a bottleneck
        for brick in bricks:
            brick.move_down(self.brick_size)

        # how to optimize? t.i.
        # ? lru cache - ball movement
        # ? update only parts of the surface

        new_ball = Ball(self.surface, 350, 400, 10, 10)
        balls.add(new_ball)

        print('LENGTH BALLS: ', len(balls))

        self.next_level = False

    def handle_shots(self, balls):
        self.shot_counter += 1
        if self.shot_counter < len(balls):
            balls.sprites()[self.shot_counter].game_on = True
        else:
            pygame.time.set_timer(self.ball_timer, 0)
            self.shot_counter = 0

    def handle_collisions(self, balls, bricks):
        collision = pygame.sprite.groupcollide(balls, bricks, False, False)
        for ball, bricks_hit in collision.items():
            for brick in bricks_hit:
                brick.number -= 1
                if brick.number <= 0:
                    bricks.remove(brick)


            # if len(bricks_hit) == 1:
            #     brick = bricks_hit[0]

            #     if brick.rect.centerx:
            #         pass

            ball.vy = -10
