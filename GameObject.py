import random
import pygame
from Ball import Ball
from Brick import Brick
import sys


class GameObject():

    def __init__(self, bricks_x=7, bricks_y=11, brick_size=60):
        print('Game!')
        random.seed()
        # self.screen = {'': int}

        self.balls = pygame.sprite.Group()
        self.bricks = pygame.sprite.Group()
        self.ball_rect = pygame.Rect(330, 380, 40, 40)

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

    def update(self):
        color = (10, 50, 30)
        self.surface.fill(color)
        self.balls.update(self.surface)
        self.bricks.update(self.surface)
        pygame.display.update()

        if {ball.game_on for ball in self.balls} == {False}:
            self.game_on = False

    def generate_next_level(self):
        print("GENERATE!!!!!!!!!!!!!!!!!!!!!!!")
        self.level += 1
        # add new bricks
        new_bricks_count = random.randint(1, self.bricks_x-2)
        positions_x = random.sample(range(0, self.bricks_x), new_bricks_count)
        # create rect inside Brick class in init, pass brick
        for i in range(new_bricks_count):
            # (30, 240, 20)
            color = (255-255//self.level, 255//self.level, 0)
            self.bricks.add(Brick(pygame.Rect(positions_x[i]*self.brick_size, 0, self.brick_size, self.brick_size), number=self.level, color=color))

        # not a bottleneck
        # rescale color
        for brick in self.bricks:
            brick.move_down(self.brick_size)

            if brick.rect.y >= (self.bricks_y-6)*self.brick_size:
                # exit(0)
                self.bricks.empty()
                self.balls.empty()
                self.level = 0
                return

        # how to optimize? t.i.
        # ? lru cache - ball movement
        # ? update only parts of the surface

        new_ball = Ball(self.surface, 350, 400, 10, 10)
        self.balls.add(new_ball)

        print('LENGTH self.balls: ', len(self.balls))

        self.next_level = False

    def handle_shots(self):
        self.shot_counter += 1
        if self.shot_counter < len(self.balls):
            # self.balls.set_game_on(self.shot_counter)
            self.balls.sprites()[self.shot_counter].game_on = True
        else:
            pygame.time.set_timer(self.ball_timer, 0)
            self.shot_counter = 0

    def handle_collisions(self):
        collisions = pygame.sprite.groupcollide(self.balls, self.bricks, False, False)
        for ball, bricks_hit in collisions.items():
            self.handle_single_collision(ball, bricks_hit)

    def handle_single_collision(self, ball, bricks_hit):
        if len(bricks_hit) == 2:
            print('HEEEEEY, 2 BRICKS AT ONCE!')
            if (bricks_hit[0].rect.center[1] - ball.rect.center[1]) * \
               (bricks_hit[1].rect.center[1] - ball.rect.center[1]) > 0:
                ball.vy = -ball.vy
            else:
                ball.vx = -ball.vx
        else:
            # refactor
            brick = bricks_hit[0]
            if ball.vx >= 0 and ball.vy >= 0:
                if brick.rect.collidepoint(ball.rect.midright):
                    print('to the left!')
                    ball.vx = -ball.vx
                elif brick.rect.collidepoint(ball.rect.midbottom):
                    print('to the top!')
                    ball.vy = -ball.vy
                elif brick.rect.collidepoint(ball.rect.bottomleft):
                    print('to the top!')
                    ball.vy = -ball.vy
                elif brick.rect.collidepoint(ball.rect.topright):
                    print('to the left!')
                    ball.vx = -ball.vx
                else:
                    print("that's complicated!")
                    ball.vx = -ball.vx
                    ball.vy = -ball.vy
            elif ball.vx >= 0 and ball.vy <= 0:
                if brick.rect.collidepoint(ball.rect.midright):
                    print('to the left!')
                    ball.vx = -ball.vx
                elif brick.rect.collidepoint(ball.rect.midtop):
                    print('to the bottom!')
                    ball.vy = -ball.vy
                elif brick.rect.collidepoint(ball.rect.bottomleft):
                    print('to the left!')
                    ball.vx = -ball.vx
                elif brick.rect.collidepoint(ball.rect.topleft):
                    print('to the bottom!')
                    ball.vy = -ball.vy
                else:
                    print("that's complicated!")
                    ball.vx = -ball.vx
                    ball.vy = -ball.vy
            elif ball.vx <= 0 and ball.vy <= 0:
                if brick.rect.collidepoint(ball.rect.midleft):
                    print('to the right!')
                    ball.vx = -ball.vx
                elif brick.rect.collidepoint(ball.rect.midtop):
                    print('to the bottom!')
                    ball.vy = -ball.vy
                elif brick.rect.collidepoint(ball.rect.bottomleft):
                    print('to the right!')
                    ball.vx = -ball.vx
                elif brick.rect.collidepoint(ball.rect.topright):
                    print('to the bottom!')
                    ball.vy = -ball.vy
                else:
                    print("that's complicated!")
                    ball.vx = -ball.vx
                    ball.vy = -ball.vy
            else:  # ball.vx <= 0 and ball.vy >= 0
                if brick.rect.collidepoint(ball.rect.midleft):
                    print('to the right!')
                    ball.vx = -ball.vx
                elif brick.rect.collidepoint(ball.rect.midbottom):
                    print('to the top!')
                    ball.vy = -ball.vy
                elif brick.rect.collidepoint(ball.rect.bottomright):
                    print('to the top!')
                    ball.vy = -ball.vy
                elif brick.rect.collidepoint(ball.rect.topleft):
                    print('to the right!')
                    ball.vx = -ball.vx
                else:
                    print("that's complicated!")
                    ball.vx = -ball.vx
                    ball.vy = -ball.vy

        # add more strict tolerance for double brick hit/removal
        for brick in bricks_hit:
            brick.number -= 1
            if brick.number <= 0:
                self.bricks.remove(brick)
            else:
                # color, number, level
                # update color
                pass
                # updated_color = list(brick.color)
                # print('color before update: ', updated_color)
                # updated_color[0] -= 255//(brick.number+1)
                # updated_color[1] += 255//(brick.number+1)

                # brick.color = tuple(updated_color)
                # print('color after update: ', brick.color)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if self.game_on:
                if event.type == self.ball_timer:
                    self.handle_shots()
            else:
                self.handle_mouse_events(event)

    def handle_mouse_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseButtons = pygame.mouse.get_pressed()
            if mouseButtons[0] == 1:
                self.start_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            # delete line of shot direction
            if self.start_pos and pygame.mouse.get_pressed()[0] == 0:
                self.end_pos = event.pos
                if self.end_pos[1] > self.start_pos[1]:
                    self.strike()

        if event.type == pygame.MOUSEMOTION:
            # pressed - draw line shot direction
            if pygame.mouse.get_pressed()[0] == 1:
                intermediate_pos = event.pos
                # print(intermediate_pos)
            if self.ball_rect.collidepoint(event.pos):
                pygame.mouse.set_cursor(*pygame.cursors.diamond)
            else:
                pygame.mouse.set_cursor(*pygame.cursors.arrow)

    def strike(self):
        # at the beginning calculate once and set for all self.balls
        # fcn collisions with bricks
        for ball in self.balls:
            ball.calculateVelocity(self.start_pos, self.end_pos)
        self.game_on = True
        self.next_level = True
        pygame.time.set_timer(self.ball_timer, 150)
        self.balls.sprites()[0].game_on = True
