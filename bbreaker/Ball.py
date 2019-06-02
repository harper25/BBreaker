import math
import pygame
import random


class Ball(pygame.sprite.Sprite):
    init_position = [None, None]
    shot_counter = 0
    init_speed = 10
    init_velocity = [0, 0]

    def __init__(self, surface, speed=init_speed, size=10):
        pygame.sprite.Sprite.__init__(self)
        self.screen_width, self.screen_height = \
            pygame.display.get_surface().get_size()
        self.x = Ball.init_position[0]
        self.y = Ball.init_position[1]
        self.speed = speed
        self.vx = 0
        self.vy = 0
        self.size = size
        self.game_on = False
        self.color = (255, 255, 255)

    @classmethod
    def set_initial_velocity(cls, strike_angle):
        cls.init_velocity[0] = round(cls.init_speed * math.cos(strike_angle))
        cls.init_velocity[1] = round(cls.init_speed * math.sin(strike_angle))
        cls.init_position[0] = None

    @staticmethod
    def calculate_strike_angle(start_pos, end_pos):
        if end_pos[1] < start_pos[1]:
            return None

        delta = [start_pos[0]-end_pos[0], start_pos[1]-end_pos[1]]
        strike_angle = math.atan2(delta[1], delta[0])
        min_angle = math.radians(10)

        if strike_angle < -math.pi + min_angle or strike_angle > -min_angle:
            return None

        return strike_angle

    def update(self, surface):
        if self.game_on:
            # check borders
            if self.x < self.size/2:
                self.vx = abs(self.vx)
            elif self.x > self.screen_width - self.size/2:
                self.vx = -abs(self.vx)
            if self.y < self.size/2:
                self.vy = -self.vy
            # calculate next position
            self.x = self.x + self.vx
            self.y = self.y + self.vy
            # check if ball is out of game
            if self.y > self.screen_height - 4*self.size:
                # set new x position in next round
                if not Ball.init_position[0]:
                    Ball.init_position[0] = self.x - self.vx
                self.x = Ball.init_position[0]
                self.y = Ball.init_position[1]
                self.game_on = False
        self.draw(surface)

    def draw(self, surface):
        self.rect = pygame.draw.circle(
            surface,
            self.color,
            (self.x, self.y),
            self.size)

    def bounce_from_central_corner(self):
        # calculate angles of bounce from bottom/top and side of the brick
        # chose random angle from the calculated range
        print('central corner!')
        alfa1 = math.atan2(self.vy, -self.vx)
        alfa2 = math.atan2(-self.vy, self.vx)
        if self.vx > 0:
            if alfa1 < 0:
                alfa1 = alfa1 + 2*math.pi
            else:
                alfa1 = alfa1 - 2*math.pi
        self.set_cartesian_velocity(alfa1, alfa2)

    def bounce_from_side_corner(self, direction_change):
        print('side corner!')
        # change in vy to -vy
        if direction_change:
            alfa1 = math.atan2(self.vy, self.vx)
            alfa2 = math.atan2(-self.vy, self.vx)
        else:  # change in vx to -vx
            alfa1 = math.atan2(self.vy, self.vx)
            alfa2 = math.atan2(self.vy, -self.vx)
        self.set_cartesian_velocity(alfa1, alfa2)

    def bounce_from_side_corner_special(self):
        print('side corner!')
        # change in vy to -vy
        alfa1 = math.atan2(self.vy, self.vx) + 2*math.pi
        alfa2 = math.atan2(-self.vy, self.vx)
        self.set_cartesian_velocity(alfa1, alfa2)

    def set_cartesian_velocity(self, alfa1, alfa2):
        vy = 0
        while abs(vy) < 3:
            vx, vy = self.get_cartesian_velocity(alfa1, alfa2)
        self.vx = vx
        self.vy = vy

    def get_cartesian_velocity(self, alfa1, alfa2):
        alfa_bounce = random.uniform(alfa1, alfa2)
        vx = round(self.speed * math.cos(alfa_bounce))
        vy = round(self.speed * math.sin(alfa_bounce))
        return vx, vy

    def handle_brick_collisions(self, bricks_hit):
        if len(bricks_hit) == 3:
            self.handle_three_brick_collision()
        if len(bricks_hit) == 2:
            self.handle_two_brick_collision(bricks_hit)
        else:
            self.handle_one_brick_collision(bricks_hit[0])

    def handle_three_brick_collision(self):
        print('WHOOHOAA, 3 BRICKS AT ONCE!')
        self.vy = -self.vy
        self.vx = -self.vx

    def handle_two_brick_collision(self, bricks_hit):
        print('HEEEEEY, 2 BRICKS AT ONCE!')
        if bricks_hit[0].rect.centerx == bricks_hit[1].rect.centerx:
            self.vx = -self.vx
        elif bricks_hit[0].rect.centery == bricks_hit[1].rect.centery:
            self.vy = -self.vy
        else:
            self.vx = -self.vx
            self.vy = -self.vy

    def handle_one_brick_collision(self, brick):
        if self.vx >= 0 and self.vy >= 0:
            if brick.rect.collidepoint(self.rect.midright):
                self.vx = -self.vx
            elif brick.rect.collidepoint(self.rect.midbottom):
                self.vy = -self.vy
            elif brick.rect.collidepoint(self.rect.bottomleft):
                self.bounce_from_side_corner(1)
            elif brick.rect.collidepoint(self.rect.topright):
                self.bounce_from_side_corner(0)
            else:
                self.bounce_from_central_corner()

        elif self.vx >= 0 and self.vy <= 0:
            if brick.rect.collidepoint(self.rect.midright):
                self.vx = -self.vx
            elif brick.rect.collidepoint(self.rect.midtop):
                self.vy = -self.vy
            elif brick.rect.collidepoint(self.rect.bottomleft):
                self.bounce_from_side_corner(0)
            elif brick.rect.collidepoint(self.rect.topleft):
                self.bounce_from_side_corner(1)
            else:
                self.bounce_from_central_corner()

        elif self.vx <= 0 and self.vy <= 0:
            if brick.rect.collidepoint(self.rect.midleft):
                self.vx = -self.vx
            elif brick.rect.collidepoint(self.rect.midtop):
                self.vy = -self.vy
            elif brick.rect.collidepoint(self.rect.bottomleft):
                self.bounce_from_side_corner(0)
            elif brick.rect.collidepoint(self.rect.topright):
                self.bounce_from_side_corner_special()
            else:
                self.bounce_from_central_corner()

        else:  # self.vx <= 0 and self.vy >= 0
            if brick.rect.collidepoint(self.rect.midleft):
                self.vx = -self.vx
            elif brick.rect.collidepoint(self.rect.midbottom):
                self.vy = -self.vy
            elif brick.rect.collidepoint(self.rect.bottomright):
                self.bounce_from_side_corner(1)
            elif brick.rect.collidepoint(self.rect.topleft):
                self.bounce_from_side_corner(0)
            else:
                self.bounce_from_central_corner()
