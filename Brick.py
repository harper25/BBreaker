import pygame


class Brick(pygame.sprite.Sprite):
    def __init__(self, rect, number, color=(30, 240, 30), border_width=4):
        pygame.sprite.Sprite.__init__(self)
        self.rect = rect
        self.number = number
        self.color = color
        self.border_width = border_width

    def draw(self, surface):
        # surface fill and surface blit?
        black = (0, 0, 0)
        surface.fill(self.color, self.rect)
        surface.fill(black, self.rect.inflate(-2*self.border_width, -2*self.border_width))
        # print(self.number)
        # print(self.rect.size)
        # print(self.rect.top, self.rect.left)

        position = (self.rect.left + self.rect.width//2,
                    self.rect.top + self.rect.height//2)
        # print(position)

        text = Text(self.number)

        text.show(surface, position)

    # update
    def update(self, surface):
        self.draw(surface)

    def move_down(self, brick_size):
        # not a bottleneck
        self.rect.y += brick_size

    def rescale_color(self, level):
        # regular bricks
        if self.number <= level:
            updated_color = list(self.color)
            change = (level - self.number) * 255//level
            updated_color[0] = 255 - change
            updated_color[1] = change
            self.color = tuple(updated_color)


class Text:
    def __init__(self, message, size=22, font_name="comicsansms"):
        self.message = str(message)
        self.size = size
        self.font_name = font_name
        self.font = pygame.font.SysFont(self.font_name, self.size)

    def show(self, surface, position, color=(255, 255, 255)):
        text = self.font.render(self.message, 0, color)  # ?
        # font = pygame.font.Font(None, 25)  # ?

        text_rect = text.get_rect(center=position)
        surface.blit(text, text_rect)