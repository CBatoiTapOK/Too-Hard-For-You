import pygame, os, math
from .obb_collision import OBB

IMG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "images")

class Proj:
    obstacles = {
        "Fireball": pygame.image.load(os.path.join(IMG_DIR, "fireball.png")),
        "Arrow": pygame.image.load(os.path.join(IMG_DIR, "arrow.png")),
    }
    def __init__(self, x, y, obs_type, end_loc, speed, offscreen_disable = False, size=1):
        self.x = x
        self.y = y
        self.obs_type = obs_type
        self.img = pygame.transform.scale(self.obstacles[obs_type], (self.obstacles[obs_type].get_width()*size, self.obstacles[obs_type].get_height()*size))
        self._img = pygame.transform.scale(self.obstacles[obs_type], (self.obstacles[obs_type].get_width()*size, self.obstacles[obs_type].get_height()*size))
        self.img_size = (self.obstacles[obs_type].get_width()*size, self.obstacles[obs_type].get_height()*size)
        self.size = size
        self.start_v = pygame.Vector2(self.x, self.y)
        self.end_v = pygame.Vector2(end_loc)
        self.speed = speed

        self.rotation = math.degrees(math.atan2(y-end_loc[1], end_loc[0]-x))
        self.rotated = False
        self.orig_img = self.img
        self.img = pygame.transform.rotate(self.img, self.rotation)

        self.offscreen_disable = offscreen_disable

        self.rect = OBB((self.x+self.img.get_width()*0.5, self.y+self.img.get_height()*0.5), (self.img.get_width()*0.5, self.img.get_height()*0.5), -self.rotation)

    def render(self, win):
        win.blit(self.img, (self.x, self.y))

    def move(self):
        try:# на случай нулевого вектора
            vel = (self.end_v-self.start_v).normalize()*self.speed
        except:
            vel = (self.end_v-self.start_v)
            vel.x += 1
            vel = vel.normalize()*self.speed

        self.x += vel.x
        self.y += vel.y
        self.rect.center.x, self.rect.center.y = self.x+self.img.get_width()*0.5, self.y+self.img.get_height()*0.5

    def off_screen(self, obs_list, screen_size, return_val=False):
        if (self.x < -self.img_size[0] or self.x > screen_size[0] or self.y < -self.img_size[1] or self.y > screen_size[1]) and not self.offscreen_disable:
            try:
                obs_list.remove(self)
            except:
                pass
        elif self.offscreen_disable and return_val:
            return self.x < -self.img_size[0] or self.x > screen_size[0] or self.y < -self.img_size[1] or self.y > screen_size[1]

        return obs_list
