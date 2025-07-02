import pygame
from typing import List, Tuple, Optional
from constantes import Constantes

class GameOverScreen:
    def __init__(self, tela: pygame.Surface) -> None:
        self._tela = tela
        self._fonte: pygame.font.Font = pygame.font.Font(None, 50)
        self._fonte_titulo: pygame.font.Font = pygame.font.Font(None, 100) 
        self._opcoes: List[str] = ["Continuar", "Novo Jogo", "Sair para Menu"]
        self._selecionado: int = 0
        self._botoes_rects: List[pygame.Rect] = []

    def desenhar(self) -> None:
        self._tela.fill((20, 0, 0))
        titulo: pygame.Surface = self._fonte_titulo.render("Você Morreu", True, Constantes.VERMELHO)
        titulo_rect = titulo.get_rect(center=(Constantes.LARGURA // 2, Constantes.ALTURA * 0.3)) 
        self._tela.blit(titulo, titulo_rect)

        self._botoes_rects = []
        y_inicial = Constantes.ALTURA * 0.5
        espacamento = 80 

        for i, texto in enumerate(self._opcoes):
            cor: Tuple[int, int, int] = Constantes.COR_SELECIONADA if i == self._selecionado else Constantes.COR_TEXTO
            opcao_surf: pygame.Surface = self._fonte.render(texto, True, cor)
            opcao_rect: pygame.Rect = opcao_surf.get_rect(center=(Constantes.LARGURA // 2, y_inicial + i * espacamento))
            self._botoes_rects.append(opcao_rect)
            self._tela.blit(opcao_surf, opcao_rect)

    def mover_selecao(self, direcao: int) -> None:
        self._selecionado = (self._selecionado + direcao) % len(self._opcoes)

    def opcao_escolhida(self) -> str:
        return self._opcoes[self._selecionado]

    def verificar_clique(self, mouse_pos: Tuple[int, int]) -> Optional[str]:
        for i, rect in enumerate(self._botoes_rects):
            if rect.collidepoint(mouse_pos):
                self._selecionado = i
                return self.opcao_escolhida()
        return None