import math
import pygame
import random


class Ball(pygame.sprite.Sprite):
    init_position = [0, 0]
    out_of_game_counter = 0

    def __init__(self, surface, speed=6, size=10):
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
            if self.x < self.size/2 or self.x > self.screen_width - self.size/2:
                self.vx = -self.vx
            if self.y < self.size/2:
                self.vy = -self.vy
            self.x = self.x + self.vx
            self.y = self.y + self.vy
            if self.y > self.screen_height - 4*self.size:
                Ball.out_of_game_counter += 1
                if Ball.out_of_game_counter == 1:
                    Ball.init_position[0] = self.x - self.vx
                self.x = Ball.init_position[0]
                self.y = Ball.init_position[1]
                self.game_on = False
        self.draw(surface, self.color)

    def draw(self, surface, color):
        self.rect = pygame.draw.circle(surface, color, (self.x, self.y), self.size)

    # classmethod?
    def calculate_init_velocity(self, start_pos, end_pos):
        delta = [start_pos[0]-end_pos[0], start_pos[1]-end_pos[1]]
        alfa = math.atan2(delta[0], delta[1])
        self.vx = round(self.speed * math.sin(alfa))
        self.vy = round(self.speed * math.cos(alfa))

    def bounce_from_central_corner(self):
        # calculate angles of bounce from bottom/top and side of the brick
        # chose random angle from the calculated range
        print('central corner!')
        alfa1 = math.atan2(self.vy, -self.vx)
        alfa2 = math.atan2(-self.vy, self.vx)
        alfa_bounce = random.uniform(alfa1, alfa2)
        self.vx = round(self.speed * math.sin(alfa_bounce))
        self.vy = round(self.speed * math.cos(alfa_bounce))

    def bounce_from_side_corner(self, direction_change):
        print('side corner!')
        # change in vy to -vy
        if direction_change:
            alfa1 = math.atan2(self.vy, self.vx)
            alfa2 = math.atan2(-self.vy, self.vx)
        else:  # change in vx to -vx
            alfa1 = math.atan2(self.vy, self.vx)
            alfa2 = math.atan2(self.vy, -self.vx)
        alfa_bounce = random.uniform(alfa1, alfa2)
        self.vx = round(self.speed * math.sin(alfa_bounce))
        self.vy = round(self.speed * math.cos(alfa_bounce))
