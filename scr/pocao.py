import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from asset_manager import AssetManager

class Pocao(pygame.sprite.Sprite):
    def __init__(self, center_pos, asset_manager: 'AssetManager'):
        super().__init__()
        
        self.image: pygame.Surface = asset_manager.get_imagem('pocao')
        self.rect: pygame.Rect = self.image.get_rect(center=center_pos)
        self._start_y = center_pos[1]
        
        self._bob_speed = 0.5
        self._bob_range = 5
        self._bob_direction = 1

    def get_rect(self) -> pygame.Rect:
        return self.rect

    def update(self, *args):
        self.rect.y += self._bob_speed * self._bob_direction
        if self.rect.y > self._start_y + self._bob_range or self.rect.y < self._start_y - self._bob_range:
            self._bob_direction *= -1

        if self.rect.right < 0:
            self.kill()