import pygame

class Button:
    def __init__(self, text, x, y, width, height, inactive_color, active_color, action=None):
        self.text = text
        self.x = x - width / 2
        self.y = y - height / 2
        self.width = width
        self.height = height
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.action = action
        self.is_selected = False

    def draw(self, screen, font):
        color = self.active_color if self.is_selected else self.inactive_color

        # pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height), 2)

        textSurf = font.render(self.text, False, color)
        textRect = textSurf.get_rect()
        textRect.center = ((self.x + (self.width / 2)), (self.y + (self.height / 2)))
        screen.blit(textSurf, textRect)
