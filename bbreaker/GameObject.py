import math
import pygame
import random
import sys

from bbreaker.Ball import Ball
from bbreaker.Brick import Brick


class GameObject():

    def __init__(self, bricks_x=7, bricks_y=11, brick_size=60):
        random.seed()
        # self.screen = {'': int}

        self.balls = pygame.sprite.Group()
        self.bricks = pygame.sprite.Group()

        self.settings = {'bricks_number': (bricks_x, bricks_y),
                         'brick_size': brick_size,
                         'screen_size': (brick_size*bricks_x,
                                         brick_size*bricks_y,)}

        self.surface = pygame.display.set_mode(self.settings['screen_size'])
        self.game_on = False
        self.next_level = True
        self.level = 0
        Ball.shot_timer = pygame.USEREVENT + 1
        Ball.shot_counter = 0
        Ball.init_position = [self.settings['screen_size'][0]//2,
                              (self.settings['bricks_number'][1] - 1)
                              * self.settings['brick_size']]

    def update(self):
        color = (20, 10, 30)
        self.surface.fill(color)
        self.balls.update(self.surface)
        self.bricks.update(self.surface)
        pygame.display.update()
        if {ball.game_on for ball in self.balls} == {False}:
            self.game_on = False

    def generate_next_level(self):
        self.level += 1
        bricks_x = self.settings['bricks_number'][0]
        bricks_y = self.settings['bricks_number'][1]

        brick_size = self.settings['brick_size']
        new_bricks_count = random.randint(1, bricks_x-2)
        positions_x = random.sample(range(0, bricks_x), new_bricks_count)
        for i in range(new_bricks_count):
            rect = pygame.Rect(positions_x[i]*brick_size,
                               0,
                               brick_size-2,
                               brick_size-2)
            self.bricks.add(Brick(rect, number=self.level, color=(0, 0, 150)))
        for brick in self.bricks:
            brick.move_down(brick_size)
            brick.rescale_color(self.level)
            if brick.rect.y >= (bricks_y-2)*brick_size:
                self.bricks.empty()
                self.balls.empty()
                self.level = 0
                return
        new_ball = Ball(self.surface, 10, 10)
        new_ball.draw(self.surface)
        self.balls.add(new_ball)
        self.next_level = False

    def handle_shots(self):
        # next? generator?
        Ball.shot_counter += 1
        if Ball.shot_counter < len(self.balls):
            self.balls.sprites()[Ball.shot_counter].game_on = True
        else:
            pygame.time.set_timer(Ball.shot_timer, 0)
            Ball.shot_counter = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if self.game_on:
                if event.type == Ball.shot_timer:
                    self.handle_shots()
            else:
                self.handle_mouse_events(event)

    def handle_mouse_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.mouse.set_cursor(*pygame.cursors.broken_x)
            mouseButtons = pygame.mouse.get_pressed()
            if mouseButtons[0] == 1:
                self.start_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            pygame.mouse.set_cursor(*pygame.cursors.arrow)
            if self.start_pos and pygame.mouse.get_pressed()[0] == 0:
                self.end_pos = event.pos
                self.strike()

        if event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[0] == 1:
                # pressed - draw line shot direction
                pass

    def strike(self):
        strike_angle = Ball.calculate_strike_angle(
            self.start_pos, self.end_pos)

        if not strike_angle:
            return

        Ball.set_initial_velocity(strike_angle)

        for ball in self.balls:
            ball.vx, ball.vy = Ball.init_velocity

        self.game_on = True
        self.next_level = True
        self.balls.sprites()[0].game_on = True
        pygame.time.set_timer(Ball.shot_timer, 150)

    def handle_collisions(self):
        brick_collisions = pygame.sprite.groupcollide(
            self.balls,
            self.bricks,
            False,
            False)
        for ball, bricks_hit in brick_collisions.items():
            ball.handle_brick_collisions(bricks_hit)
            self.handle_collided_bricks(bricks_hit)

    def handle_collided_bricks(self, bricks_hit):
        # add more strict tolerance for double brick hit/removal
        for brick in bricks_hit:
            brick.number -= 1
            if brick.number <= 0:
                self.bricks.remove(brick)
            else:
                brick.rescale_color(self.level)
