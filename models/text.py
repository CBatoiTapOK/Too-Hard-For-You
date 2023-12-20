class Text:
    def __init__(self, text, x, y, font, color):
        self.text = text
        self.font = font
        self.color = color
        self.text_surface = self.font.render(self.text, False, self.color)
        self.x = x - self.text_surface.get_width() // 2
        self.y = y - self.text_surface.get_height() // 2

    def draw(self, screen):
        screen.blit(self.text_surface, (self.x, self.y))
