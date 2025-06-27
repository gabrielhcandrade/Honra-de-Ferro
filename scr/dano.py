import pygame
from constantes import Constantes

class DanoPopup(pygame.sprite.Sprite):
    def __init__(self, texto: str, pos: tuple[int, int], cor: tuple[int, int, int] = Constantes.VERMELHO):
        super().__init__()
        fonte = pygame.font.SysFont(None, 30, bold=True)
        self.image = fonte.render(texto, True, cor)
        self.rect = self.image.get_rect(center=pos)
        self.lifespan = 30 
        self.move_speed = 1

    def update(self):
        self.rect.y -= self.move_speed
        self.lifespan -= 1
        if self.lifespan <= 0:
            self.kill()