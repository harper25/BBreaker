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
        self.draw(surface, self.color)

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
        self.draw(surface, self.color)

    def draw(self, surface, color):
        self.rect = pygame.draw.circle(surface,
                                       color,
                                       (self.x, self.y),
                                       self.size)

    @staticmethod
    def calculate_strike_angle(start_pos, end_pos):
        delta = [start_pos[0]-end_pos[0], start_pos[1]-end_pos[1]]
        return math.atan2(delta[1], delta[0])

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
