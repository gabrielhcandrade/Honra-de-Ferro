import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from asset_manager import AssetManager

class Pocao(pygame.sprite.Sprite):
    """
    Representa uma poção de vida que o jogador pode coletar.
    """
    def __init__(self, center_pos, asset_manager: 'AssetManager'):
        super().__init__()
        
        # Obtém a imagem do AssetManager
        self.image: pygame.Surface = asset_manager.get_imagem('pocao')
        self.rect = self.image.get_rect(center=center_pos)
        self.start_y = center_pos[1]
        
        # Atributos para o efeito de flutuação
        self.bob_speed = 0.5
        self.bob_range = 5
        self.bob_direction = 1

    def update(self, *args):
        """
        Atualiza a posição da poção, criando um efeito de flutuação.
        """
        # Efeito de flutuar (bob)
        self.rect.y += self.bob_speed * self.bob_direction
        if self.rect.y > self.start_y + self.bob_range or self.rect.y < self.start_y - self.bob_range:
            self.bob_direction *= -1

        # Remove a poção se ela sair da tela
        if self.rect.right < 0:
            self.kill()