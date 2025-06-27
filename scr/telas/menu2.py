import pygame
from typing import Tuple, TYPE_CHECKING

# Adicionado para evitar importação circular, mas permitir anotações de tipo
if TYPE_CHECKING:
    from asset_manager import AssetManager

class Menu2:
    # CORREÇÃO: O construtor __init__ foi atualizado para aceitar o asset_manager.
    def __init__(self, tela: pygame.Surface, asset_manager: 'AssetManager') -> None:
        self.tela = tela
        # CORREÇÃO: A imagem de fundo agora é obtida do asset_manager.
        self.background_menu_2: pygame.Surface = asset_manager.get_imagem('fundo2')
        self.fonte: pygame.font.Font = pygame.font.Font(None, 36)

    def desenhar(self) -> None:
        self.tela.blit(self.background_menu_2, (0, 0))