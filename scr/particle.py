import pygame
import random
from typing import Tuple

class Particle(pygame.sprite.Sprite):
    def __init__(self, pos: Tuple[int, int], cor: Tuple[int, int, int], direcao: Tuple[float, float] = (0,0)):
        super().__init__()
        self._x, self._y = pos

        self._vx = direcao[0] + random.uniform(-2, 2)
        self._vy = direcao[1] + random.uniform(-3, 1)
        self._rad = random.randint(4, 7)
        self._cor = cor
        self._lifespan = random.randint(15, 25)

    def update(self):
        self._x += self._vx
        self._y += self._vy
        self._lifespan -= 1
        self._rad -= 0.2
        if self._rad <= 0 or self._lifespan <= 0:
            self.kill()

    def draw(self, tela: pygame.Surface):
        if self._rad > 0:
            pygame.draw.circle(tela, self._cor, (int(self._x), int(self._y)), int(self._rad))