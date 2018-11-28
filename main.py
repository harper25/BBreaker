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
        # if game.level == 0:
        #     welcomome_menu()
        # else:
        # get if not balls in game and get if generate next level
        if not game.game_on and game.next_level:
            game.generate_next_level()
        game.handle_events()
        game.handle_collisions()
        game.update()
        FPS_CLOCK.tick(FPS)


if __name__ == "__main__":
    main()


# distance = math.hypot(x1 - x2, y1 - y2)
# pygame.mouse.set_cursor(*pygame.cursors.sizer_x_strings)
# *pygame.cursors.broken_x - złapanie do celowania
# *pygame.cursors.tri_left - ładny do przycisków i ogólnie
