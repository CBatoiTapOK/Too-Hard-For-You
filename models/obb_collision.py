import pygame

class OBB:
    def __init__(self, center, size, angle):
        self.center = pygame.Vector2(center)
        self.size = pygame.Vector2(size)
        self.angle = angle

        # utility vectors for calculating corner of bounding box
        self._tl = pygame.Vector2(-self.size.x / 2, self.size.y / 2)
        self._tr = pygame.Vector2(self.size.x / 2, self.size.y / 2)
        self._bl = pygame.Vector2(-self.size.x / 2, -self.size.y / 2)
        self._br = pygame.Vector2(self.size.x / 2, -self.size.y / 2)

    @classmethod
    def from_rect(cls, rect:pygame.Rect):
        center = pygame.Vector2(rect.center)
        size = pygame.Vector2(rect.size)
        return cls(center, size, 0)

    @property
    def orientation(self) -> pygame.Vector2:
        o = pygame.Vector2()
        o.from_polar((1, self.angle))
        return o

    @property
    def topleft(self) -> pygame.Vector2:
        return self.center + self._tl.rotate(self.angle)

    @property
    def topright(self) -> pygame.Vector2:
        return self.center + self._tr.rotate(self.angle)

    @property
    def bottomleft(self) -> pygame.Vector2:
        return self.center + self._bl.rotate(self.angle)

    @property
    def bottomright(self) -> pygame.Vector2:
        return self.center + self._br.rotate(self.angle)

    def corners(self):
        return iter((self.topleft, self.topright, self.bottomright, self.bottomleft))

    def collideobb(self, obb):
        axes = iter((self.orientation, self.orientation.rotate(90), obb.orientation, obb.orientation.rotate(90)))
        for ax in axes:
            min_along1, max_along1 = 1E10, -1E10
            min_along2, max_along2 = 1E10, -1E10
            for corner in self.corners():
                p = ax.dot(corner)
                if p > max_along1:
                    max_along1 = p
                if p < min_along1:
                    min_along1 = p
            for corner in obb.corners():
                p = ax.dot(corner)
                if p > max_along2:
                    max_along2 = p
                if p < min_along2:
                    min_along2 = p
            if min_along1 <= max_along2 and max_along1 >= min_along2:
                continue
            return False
        return True

    def colliderect(self, rect):
        return self.collideobb(OBB.from_rect(rect))
