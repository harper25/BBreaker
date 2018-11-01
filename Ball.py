import pygame
import math


class Ball(pygame.sprite.Sprite):
    def __init__(self, surface, x, y, speed=10, size=10):
        pygame.sprite.Sprite.__init__(self)
        self.screen_width, self.screen_height = \
            pygame.display.get_surface().get_size()
        self.x = x
        self.y = y
        self.speed = speed
        self.vx = 0
        self.vy = 0
        self.size = size
        self.game_on = False
        self._color = (255, 255, 255)
        self.draw(surface, self._color)

    def update(self, surface):
        # future: draw_background() before the call to Ball.move()
        self.draw(surface, (0, 0, 0))
        if self.x < self.size/2 or self.x > self.screen_width - self.size/2:
            self.vx = -self.vx
        if self.y < self.size/2:
            self.vy = -self.vy
        if self.y > self.screen_height - 2*self.size:
            self.x = 350
            self.y = 400
            self.game_on = False

        self.x = self.x + self.vx
        self.y = self.y + self.vy
        self.draw(surface, (255, 255, 255))

    def draw(self, surface, color):
        pygame.draw.circle(surface, color, (self.x, self.y), self.size)

    def calculateVelocity(self, start_pos, end_pos):
        delta = list([start_pos[0]-end_pos[0], start_pos[1]-end_pos[1]])
        # print("Delta: ", delta)
        alfa = math.atan2(delta[0], delta[1])
        self.vx = round(self.speed * math.sin(alfa))
        self.vy = round(self.speed * math.cos(alfa))



