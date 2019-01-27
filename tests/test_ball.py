from bbreaker.Ball import Ball
import math
import numpy


def AlmostEqual(a, b, digits=3):
    epsilon = 10 ** -digits
    assert abs(a - b) < epsilon


def test_calculate_strike_angle():
    AlmostEqual(math.cos(Ball.calculate_strike_angle((5, 10), (10, 10))), 1)
    AlmostEqual(math.cos(Ball.calculate_strike_angle((5, 10), (5, 0))), 0)
    AlmostEqual(math.cos(Ball.calculate_strike_angle((5, 10), (0, 10))), -1)
    AlmostEqual(math.cos(Ball.calculate_strike_angle((5, 10), (5, 15))), 0)

    AlmostEqual(math.sin(Ball.calculate_strike_angle((5, 10), (10, 10))), 0)
    AlmostEqual(math.sin(Ball.calculate_strike_angle((5, 10), (5, 0))), 1)
    AlmostEqual(math.sin(Ball.calculate_strike_angle((5, 10), (0, 10))), 0)
    AlmostEqual(math.sin(Ball.calculate_strike_angle((5, 10), (5, 15))), -1)
