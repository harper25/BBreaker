from GameObject import GameObject

import pygame


game = GameObject()

# easy medium hard - probability of high number of boxes each round
FPS = 60
FPS_CLOCK = pygame.time.Clock()

pygame.init()
pygame.display.set_caption('B-Breaker!')


def main():
    while True:
        # get if not balls in game and get if generate next level
        if not game.game_on and game.next_level:
            game.generate_next_level()
        game.handle_events()
        game.handle_collisions()
        game.update()
        FPS_CLOCK.tick(FPS)


if __name__ == "__main__":
    main()


# x1, y1 = position
# x2, y2 = self.circle.center
# distance = math.hypot(x1 - x2, y1 - y2)

# pygame.mouse.set_cursor(*pygame.cursors.sizer_x_strings)
# *pygame.cursors.broken_x - złapanie do celowania
# *pygame.cursors.tri_left - ładny do przycisków i ogólnie

# os.environ['SDL_VIDEO_CENTERED'] = '1'

# r1 = pygame.draw.rect(DISPLAYSURF, WHITE, (100, 100, 50, 50))
# r2 = pygame.draw.rect(DISPLAYSURF, (255, 255, 0), (200, 200, 50, 50), 5)
# if r1.collidepoint(event.pos):
#     pygame.draw.rect(DISPLAYSURF, (0, 255, 0), r1)
# if r2.collidepoint(event.pos):
#     # pygame.draw.rect(DISPLAYSURF, red, r2)
#     pygame.draw.rect(DISPLAYSURF, (255, 0, 0), (200, 200, 50, 50), 20)