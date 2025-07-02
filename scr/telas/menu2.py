import pygame
from typing import Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from asset_manager import AssetManager

class Menu2:
    def __init__(self, tela: pygame.Surface, asset_manager: 'AssetManager') -> None:
        self._tela = tela
        self._background_menu_2: pygame.Surface = asset_manager.get_imagem('fundo2')
        self._fonte: pygame.font.Font = pygame.font.Font(None, 36)

    def desenhar(self) -> None:
        self._tela.blit(self._background_menu_2, (0, 0))