import pygame


class Brick(pygame.sprite.Sprite):
    # should pass position here, not rect
    def __init__(self, rect, number, color=None, border_width=4):
        pygame.sprite.Sprite.__init__(self)
        self.rect = rect
        self.number = number
        self.border_width = border_width
        self.color = color if color else [30, 240, 30]

    def draw(self, surface):
        # surface fill and surface blit?
        pygame.draw.rect(
            surface,
            self.color,
            self.rect,
            self.border_width,
            border_radius=5,
            )
        position = self.rect.center
        text = Text(self.number)
        text.show(surface, position)

    def update(self, surface):
        self.draw(surface)

    def move_down(self, brick_size):
        self.rect.y += brick_size

    def rescale_color(self, level):
        # regular bricks
        if self.number <= level:
            change = (level - self.number) * 255//level
            self.color[0] = 255 - change
            self.color[1] = change


class Text:
    def __init__(self, message, size=22, font_name="comicsansms"):
        self.message = str(message)
        self.size = size
        self.font_name = font_name
        self.font = pygame.font.SysFont(self.font_name, self.size)

    def show(self, surface, position, color=(255, 255, 255)):
        text = self.font.render(self.message, 0, color)
        text_rect = text.get_rect(center=position)
        surface.blit(text, text_rect)
