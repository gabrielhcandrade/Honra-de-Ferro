import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from asset_manager import AssetManager

class Pocao(pygame.sprite.Sprite):

    def __init__(self, center_pos, asset_manager: 'AssetManager'):
        super().__init__()
        
        self.image: pygame.Surface = asset_manager.get_imagem('pocao')
        self.rect = self.image.get_rect(center=center_pos)
        self.start_y = center_pos[1]
        
        self.bob_speed = 0.5
        self.bob_range = 5
        self.bob_direction = 1

    def update(self, *args):
       
        self.rect.y += self.bob_speed * self.bob_direction
        if self.rect.y > self.start_y + self.bob_range or self.rect.y < self.start_y - self.bob_range:
            self.bob_direction *= -1

        if self.rect.right < 0:
            self.kill()