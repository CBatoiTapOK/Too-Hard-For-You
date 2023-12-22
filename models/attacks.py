import random, time, pygame, math
from .proj import Proj

class Attacks:
    def __init__(self):
        self.pattern = 0
        self.attack_timer = 0
        self.next_attack = random.randint(0, 3)
        self.last_attack = 0
        self.projs = []
        self.shoot_cooldown = 0
        self.attack_change_cooldown = 2
        self.hard_mode = False
        self.hard_mode_timer = 0
        self.pre_hard_mode = False
        self.extra_attacks = 5
        self.offset = 0
        self.rotate_dir = 0
        self.shot_dir = 0
        self.edge = 0


    def attack(self, player, screen_size):
        hard_time = 30
        if time.time()-self.attack_timer >= self.attack_change_cooldown:
            self.attack_timer = time.time()
            self.last_attack = self.pattern

            self.pattern = self.next_attack
            self.next_attack = random.randint(0, 3)

            if random.randint(0, 5) == 0 and not self.hard_mode and not self.pre_hard_mode and time.time()-player.spawned >= 1.5:
                self.projs = []
                self.hard_mode = True
                self.extra_attacks = int(player.score / 20)
                self.hard_mode_timer = time.time()
            if not self.hard_mode:
                self.pre_hard_mode = False

        if self.hard_mode and time.time()-self.hard_mode_timer >= hard_time:
            self.hard_mode = False
            self.projs = []
            self.extra_attacks = 0
            self.pre_hard_mode = True

        if self.pattern == 0:
            if time.time() - self.attack_timer <= 0.005 and self.last_attack != 0:
                self.offset = random.uniform(0, math.pi*2)
                self.rotate_dir = random.randint(0, 1)
            if time.time()-self.shoot_cooldown >= 0.25:
                for x in range(12+self.extra_attacks):
                    rad = math.radians(x*360/(12+self.extra_attacks))+self.offset
                    x, y = screen_size[0]*0.5-Proj.obstacles["Fireball"].get_width()*0.5, screen_size[1]*0.5-Proj.obstacles["Fireball"].get_height()*0.5
                    if self.rotate_dir == 0:
                        self.projs.append(Proj(x, y, "Fireball", (x+100*math.cos(rad), y+100*math.sin(rad)), 5))
                    else:
                        self.projs.append(Proj(x, y, "Fireball", (x+100*math.sin(rad), y+100*math.cos(rad)), 5))

                self.offset += 0.1
                self.shoot_cooldown = time.time()

        elif self.pattern == 1: # Arrows
            self.shot_dir = random.randint(0, 3)
            if time.time()-self.shoot_cooldown >= 0.5:
                for _ in range(random.randint(2, 5+self.extra_attacks)):
                    # верх-низ
                    if self.shot_dir == 0:
                        x = random.randint(1, screen_size[0]-1)
                        y = -Proj.obstacles["Arrow"].get_height() # чтобы стрела смотрела вниз высота картинки с минусом
                        self.projs.append(Proj(x, y,"Arrow", (x, 100), 7))
                    elif self.shot_dir == 1:
                        x = random.randint(1, screen_size[0]-1)
                        y = screen_size[1]
                        self.projs.append(Proj(x, y,"Arrow", (x, screen_size[1]-100), 7)) # аналогично
                    # лево-право
                    elif self.shot_dir == 2:
                        x = -Proj.obstacles["Arrow"].get_width()
                        y = random.randint(1, screen_size[1]-1)
                        self.projs.append(Proj(x, y,"Arrow", (100, y), 7))
                    else:
                        x = screen_size[0]
                        y = random.randint(1, screen_size[1]-1)
                        self.projs.append(Proj(x, y,"Arrow", (screen_size[0]-100, y), 7))

                self.shoot_cooldown = time.time()

        elif self.pattern == 2:
            self.edge = random.randint(0, 1)
            if time.time()-self.shoot_cooldown >= 1/((self.extra_attacks/4)+1):
                if self.edge == 0:
                    for x in range(8):
                        rad = math.radians(x*360/8)
                        x, y = screen_size[0]*0.5-Proj.obstacles["Fireball"].get_width()*0.5, 1
                        self.projs.append(Proj(x, y,"Fireball", (x+100*math.cos(rad), y+100*math.sin(rad)), 5))
                    for x in range(8):
                        rad = math.radians(x*360/8)
                        x, y = screen_size[0]*0.5-Proj.obstacles["Fireball"].get_width()*0.5, screen_size[1]-14
                        self.projs.append(Proj(x, y,"Fireball", (x+100*math.cos(rad), y+100*math.sin(rad)), 5))
                    for x in range(8):
                        rad = math.radians(x*360/8)
                        x, y = 1, screen_size[1]*0.5-Proj.obstacles["Fireball"].get_height()*0.5
                        self.projs.append(Proj(x, y,"Fireball", (x+100*math.cos(rad), y+100*math.sin(rad)), 5))
                    for x in range(8):
                        rad = math.radians(x*360/8)
                        x, y = screen_size[0]-14, screen_size[1]*0.5-Proj.obstacles["Fireball"].get_height()*0.5
                        self.projs.append(Proj(x, y,"Fireball", (x+100*math.cos(rad), y+100*math.sin(rad)), 5))
                else:
                    for x in range(8):
                        rad = math.radians(x*360/8)
                        x, y = 1, 1
                        self.projs.append(Proj(x, y,"Fireball", (x+100*math.cos(rad), y+100*math.sin(rad)), 5))
                    for x in range(8):
                        rad = math.radians(x*360/8)
                        x, y = 1, screen_size[1]-14
                        self.projs.append(Proj(x, y,"Fireball", (x+100*math.cos(rad), y+100*math.sin(rad)), 5))
                    for x in range(8):
                        rad = math.radians(x*360/8)
                        x, y = screen_size[0]-14, 1
                        self.projs.append(Proj(x, y,"Fireball", (x+100*math.cos(rad), y+100*math.sin(rad)), 5))
                    for x in range(8):
                        rad = math.radians(x*360/8)
                        x, y = screen_size[0]-14, screen_size[1]-14
                        self.projs.append(Proj(x, y,"Fireball", (x+100*math.cos(rad), y+100*math.sin(rad)), 5))

                self.shoot_cooldown = time.time()

        elif self.pattern == 3:
            if time.time()-self.shoot_cooldown >= 1/((self.extra_attacks/10)+1):
                # верх
                x, y = screen_size[0]*0.5-Proj.obstacles["Arrow"].get_height()*0.5, -Proj.obstacles["Arrow"].get_height()
                self.projs.append(Proj(x, y,"Arrow", (player.rect.centerx-Proj.obstacles["Arrow"].get_height()*0.5, player.rect.centery-Proj.obstacles["Arrow"].get_height()*0.5), 5))

                # низ
                x, y = screen_size[0]*0.5-Proj.obstacles["Arrow"].get_height()*0.5, screen_size[1]
                self.projs.append(Proj(x, y, "Arrow", (player.rect.centerx-Proj.obstacles["Arrow"].get_height()*0.5, player.rect.centery-Proj.obstacles["Arrow"].get_height()*0.5), 5))

                # лево
                x, y = -Proj.obstacles["Arrow"].get_height(), screen_size[1]*0.5-Proj.obstacles["Arrow"].get_height()*0.5
                self.projs.append(Proj(x, y,"Arrow", (player.rect.centerx-Proj.obstacles["Arrow"].get_height()*0.5, player.rect.centery-Proj.obstacles["Arrow"].get_height()*0.5), 5))

                # право
                x, y = screen_size[0], screen_size[1]*0.5-Proj.obstacles["Arrow"].get_height()*0.5
                self.projs.append(Proj(x, y,"Arrow", (player.rect.centerx-Proj.obstacles["Arrow"].get_height()*0.5, player.rect.centery-Proj.obstacles["Arrow"].get_height()*0.5), 5))

                # верхний левй угол
                x, y = -Proj.obstacles["Arrow"].get_height(), -Proj.obstacles["Arrow"].get_height()
                self.projs.append(Proj(x, y,"Arrow", (player.rect.centerx-Proj.obstacles["Arrow"].get_height()*0.5, player.rect.centery-Proj.obstacles["Arrow"].get_height()*0.5), 5))

                # верхний нижний угол
                x, y = -Proj.obstacles["Arrow"].get_height(), screen_size[1]
                self.projs.append(Proj(x, y,"Arrow", (player.rect.centerx-Proj.obstacles["Arrow"].get_height()*0.5, player.rect.centery-Proj.obstacles["Arrow"].get_height()*0.5), 5))

                # верхний правый угол
                x, y = screen_size[0], -Proj.obstacles["Arrow"].get_height()
                self.projs.append(Proj(x, y,"Arrow", (player.rect.centerx-Proj.obstacles["Arrow"].get_height()*0.5, player.rect.centery-Proj.obstacles["Arrow"].get_height()*0.5), 5))

                # нижний правый угол
                x, y = screen_size[0], screen_size[1]
                self.projs.append(Proj(x, y,"Arrow", (player.rect.centerx-Proj.obstacles["Arrow"].get_height()*0.5, player.rect.centery-Proj.obstacles["Arrow"].get_height()*0.5), 5))

                self.shoot_cooldown = time.time()
