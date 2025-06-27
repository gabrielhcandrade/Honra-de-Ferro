import pygame
import random
from typing import Tuple

class Particle(pygame.sprite.Sprite):
    def __init__(self, pos: Tuple[int, int], cor: Tuple[int, int, int], direcao: Tuple[float, float] = (0,0)):
        super().__init__()
        self.x, self.y = pos

        self.vx = direcao[0] + random.uniform(-2, 2)
        self.vy = direcao[1] + random.uniform(-3, 1)
        self.rad = random.randint(4, 7)
        self.cor = cor
        self.lifespan = random.randint(15, 25)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifespan -= 1
        self.rad -= 0.2
        if self.rad <= 0 or self.lifespan <= 0:
            self.kill()

    def draw(self, tela: pygame.Surface):
        if self.rad > 0:
            pygame.draw.circle(tela, self.cor, (int(self.x), int(self.y)), int(self.rad))