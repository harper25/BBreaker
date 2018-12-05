import math
import pygame
import random
import sys

from Ball import Ball
from Brick import Brick


class GameObject():

    def __init__(self, bricks_x=7, bricks_y=11, brick_size=60):
        random.seed()
        # self.screen = {'': int}

        self.balls = pygame.sprite.Group()
        self.bricks = pygame.sprite.Group()

        self.bricks_x = bricks_x
        self.bricks_y = bricks_y
        self.brick_size = brick_size
        self.screen_width = self.brick_size * self.bricks_x
        self.screen_height = self.brick_size * self.bricks_y
        self.surface = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.game_on = False
        self.next_level = True
        self.level = 0
        Ball.shot_timer = pygame.USEREVENT + 1
        Ball.shot_counter = 0
        Ball.init_position = [self.screen_width//2,
                              (self.bricks_y-1)*self.brick_size]

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
        new_bricks_count = random.randint(1, self.bricks_x-2)
        positions_x = random.sample(range(0, self.bricks_x), new_bricks_count)
        for i in range(new_bricks_count):
            self.bricks.add(Brick(pygame.Rect(positions_x[i]*self.brick_size, 0, self.brick_size-2, self.brick_size-2), number=self.level, color=(0, 0, 150)))
        for brick in self.bricks:
            brick.move_down(self.brick_size)
            brick.rescale_color(self.level)
            if brick.rect.y >= (self.bricks_y-2)*self.brick_size:
                self.bricks.empty()
                self.balls.empty()
                self.level = 0
                return
        new_ball = Ball(self.surface, 10, 10)
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
        if self.end_pos[1] < self.start_pos[1]:
            return

        alfa = Ball.calculate_strike_angle(self.start_pos, self.end_pos)
        min_angle = math.radians(10)
        if alfa < -math.pi + min_angle or alfa > -min_angle:
            return

        Ball.init_velocity[0] = round(Ball.init_speed * math.cos(alfa))
        Ball.init_velocity[1] = round(Ball.init_speed * math.sin(alfa))
        Ball.init_position[0] = None

        for ball in self.balls:
            ball.vx = Ball.init_velocity[0]
            ball.vy = Ball.init_velocity[1]

        self.game_on = True
        self.next_level = True
        pygame.time.set_timer(Ball.shot_timer, 150)
        self.balls.sprites()[0].game_on = True

    def handle_collisions(self):
        collisions = pygame.sprite.groupcollide(self.balls, self.bricks, False, False)
        for ball, bricks_hit in collisions.items():
            if len(bricks_hit) == 3:
                self.handle_three_brick_collision(ball)
            if len(bricks_hit) == 2:
                self.handle_two_brick_collision(ball, bricks_hit)
            else:
                self.handle_one_brick_collision(ball, bricks_hit[0])
            self.handle_collided_bricks(bricks_hit)

    def handle_collided_bricks(self, bricks_hit):
        # add more strict tolerance for double brick hit/removal
        for brick in bricks_hit:
            brick.number -= 1
            if brick.number <= 0:
                self.bricks.remove(brick)
            else:
                brick.rescale_color(self.level)

    def handle_three_brick_collision(self, ball):
        print('WHOOHOAA, 3 BRICKS AT ONCE!')
        ball.vy = -ball.vy
        ball.vx = -ball.vx

    def handle_two_brick_collision(self, ball, bricks_hit):
        print('HEEEEEY, 2 BRICKS AT ONCE!')
        if bricks_hit[0].rect.centerx == bricks_hit[1].rect.centerx:
            ball.vx = -ball.vx
        elif bricks_hit[0].rect.centery == bricks_hit[1].rect.centery:
            ball.vy = -ball.vy
        else:
            ball.vx = -ball.vx
            ball.vy = -ball.vy

    def handle_one_brick_collision(self, ball, brick):
        if ball.vx >= 0 and ball.vy >= 0:
            if brick.rect.collidepoint(ball.rect.midright):
                ball.vx = -ball.vx
            elif brick.rect.collidepoint(ball.rect.midbottom):
                ball.vy = -ball.vy
            elif brick.rect.collidepoint(ball.rect.bottomleft):
                ball.bounce_from_side_corner(1)
            elif brick.rect.collidepoint(ball.rect.topright):
                ball.bounce_from_side_corner(0)
            else:
                ball.bounce_from_central_corner()

        elif ball.vx >= 0 and ball.vy <= 0:
            if brick.rect.collidepoint(ball.rect.midright):
                ball.vx = -ball.vx
            elif brick.rect.collidepoint(ball.rect.midtop):
                ball.vy = -ball.vy
            elif brick.rect.collidepoint(ball.rect.bottomleft):
                ball.bounce_from_side_corner(0)
            elif brick.rect.collidepoint(ball.rect.topleft):
                ball.bounce_from_side_corner(1)
            else:
                ball.bounce_from_central_corner()

        elif ball.vx <= 0 and ball.vy <= 0:
            if brick.rect.collidepoint(ball.rect.midleft):
                ball.vx = -ball.vx
            elif brick.rect.collidepoint(ball.rect.midtop):
                ball.vy = -ball.vy
            elif brick.rect.collidepoint(ball.rect.bottomleft):
                ball.bounce_from_side_corner(0)
            elif brick.rect.collidepoint(ball.rect.topright):
                ball.bounce_from_side_corner_special()
            else:
                ball.bounce_from_central_corner()

        else:  # ball.vx <= 0 and ball.vy >= 0
            if brick.rect.collidepoint(ball.rect.midleft):
                ball.vx = -ball.vx
            elif brick.rect.collidepoint(ball.rect.midbottom):
                ball.vy = -ball.vy
            elif brick.rect.collidepoint(ball.rect.bottomright):
                ball.bounce_from_side_corner(1)
            elif brick.rect.collidepoint(ball.rect.topleft):
                ball.bounce_from_side_corner(0)
            else:
                ball.bounce_from_central_corner()
