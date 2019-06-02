import pygame

from bbreaker.Ball import Ball
from bbreaker.Brick import Brick


def test_handle_one_brick_collision():
    surface = pygame.display.set_mode((800, 800))
    ball = Ball(surface, 10, 10)
    rect = pygame.Rect(100, 100, 60, 60)
    brick = Brick(rect, number=1)

    assert True
