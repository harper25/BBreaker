import pygame


from bbreaker.GameObject import GameObject


FPS = 60
FPS_CLOCK = pygame.time.Clock()

pygame.init()
pygame.display.set_caption('B-Breaker!')

game = GameObject()


def main():
    while True:
        if not game.game_on and game.next_level:
            game.generate_next_level()
        game.handle_events()
        game.handle_collisions()
        game.update()
        FPS_CLOCK.tick(FPS)


if __name__ == "__main__":
    main()
