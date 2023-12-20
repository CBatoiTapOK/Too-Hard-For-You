import pygame, time

class Player:
    def __init__(self, x, y, img, screen_width, screen_height):
        self.img = img
        self.x = x - self.img.get_width() / 2
        self.y = y - self.img.get_height() / 2
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.speed = 6

        self.score = 0

        self.spawned = time.time()
        self.blink = [time.time(), True]

        self.rect = pygame.Rect(self.x+self.img.get_width()*0.25, self.y+self.img.get_height()*0.25, 16, 16)

    def update(self, win):
        # player
        # маргание после спавна
        if time.time() - self.spawned < 1.5:
            if time.time()-self.blink[0] >= 0.1:
                self.blink[0] = time.time()
                self.blink[1] = not self.blink[1]
            if self.blink[1]:
                self.img.set_alpha(255)
            else:
                self.img.set_alpha(100)
        else:
            if self.img.get_alpha() != 255:
                self.img.set_alpha(255)
        win.blit(self.img, (self.x, self.y))

    def move(self):
        keys = pygame.key.get_pressed()
        # реализация движения с учётом границ экрвна и размеров модельки
        if keys[pygame.K_a]:
            if self.x > 0:
                self.x -= self.speed
        if keys[pygame.K_d]:
            if self.x < self.screen_width -self.img.get_width():
                self.x += self.speed
        if keys[pygame.K_w]:
            if self.y > 0:
                self.y -= self.speed
        if keys[pygame.K_s]:
            if self.y < self.screen_height -self.img.get_height():
                self.y += self.speed
        self.rect = pygame.Rect(self.x+self.img.get_width()*0.25, self.y+self.img.get_height()*0.25, 16, 16)
