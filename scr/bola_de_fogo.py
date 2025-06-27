import pygame
import math
from typing import Tuple, TYPE_CHECKING
from constantes import Constantes

if TYPE_CHECKING:
    from asset_manager import AssetManager

class BolaDeFogo(pygame.sprite.Sprite):
    def __init__(self, origem: Tuple[int, int], alvo: Tuple[int, int], asset_manager: 'AssetManager') -> None:
        super().__init__()
        
        # Imagem da bola de fogo vinda do AssetManager
        self.image: pygame.Surface = asset_manager.get_imagem('bola_de_fogo')
        self.rect: pygame.Rect = self.image.get_rect(center=origem)

        # Velocidade configurável
        velocidade = 6

        # Calcula direção normalizada para o alvo
        dx = alvo[0] - origem[0]
        dy = alvo[1] - origem[1]
        dist = math.hypot(dx, dy)

        self._vel_x = (dx / dist * velocidade) if dist else 0
        self._vel_y = (dy / dist * velocidade) if dist else 0

    def update(self, *args) -> None:
        """Atualiza a posição da bola de fogo e remove se sair da tela."""
        self.rect.x += self._vel_x
        self.rect.y += self._vel_y

        if (self.rect.right < -50 or self.rect.left > Constantes.LARGURA + 50 or
            self.rect.bottom < -50 or self.rect.top > Constantes.ALTURA + 50):
            self.kill()

    # Getters (opcional, caso precise acessar de forma segura)
    @property
    def posicao(self) -> Tuple[int, int]:
        return self.rect.center

    @property
    def velocidade(self) -> Tuple[float, float]:
        return self._vel_x, self._vel_y
