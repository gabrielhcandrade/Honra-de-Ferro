import pygame
from typing import List, Tuple, Optional

from constantes import Constantes

class GameOverScreen:
    def __init__(self, tela: pygame.Surface) -> None:
        self.tela = tela
        self.fonte: pygame.font.Font = pygame.font.Font(None, 50)
        self.fonte_titulo: pygame.font.Font = pygame.font.Font(None, 100) 
        self.opcoes: List[str] = ["Continuar", "Novo Jogo", "Sair para Menu"]
        self.selecionado: int = 0
        self.botoes_rects: List[pygame.Rect] = []

    def desenhar(self) -> None:
        """Desenha a tela de Game Over centralizada."""
        self.tela.fill((20, 0, 0))
        titulo: pygame.Surface = self.fonte_titulo.render("Você Morreu", True, Constantes.VERMELHO)
        titulo_rect = titulo.get_rect(center=(Constantes.LARGURA // 2, Constantes.ALTURA * 0.3)) 
        self.tela.blit(titulo, titulo_rect)

        self.botoes_rects = []
        y_inicial = Constantes.ALTURA * 0.5
        espacamento = 80 

        for i, texto in enumerate(self.opcoes):
            cor: Tuple[int, int, int] = Constantes.COR_SELECIONADA if i == self.selecionado else Constantes.COR_TEXTO
            opcao_surf: pygame.Surface = self.fonte.render(texto, True, cor)
            opcao_rect: pygame.Rect = opcao_surf.get_rect(center=(Constantes.LARGURA // 2, y_inicial + i * espacamento))
            self.botoes_rects.append(opcao_rect)
            self.tela.blit(opcao_surf, opcao_rect)

    def mover_selecao(self, direcao: int) -> None:
        self.selecionado = (self.selecionado + direcao) % len(self.opcoes)

    def opcao_escolhida(self) -> str:
        return self.opcoes[self.selecionado]

    def verificar_clique(self, mouse_pos: Tuple[int, int]) -> Optional[str]:
        for i, rect in enumerate(self.botoes_rects):
            if rect.collidepoint(mouse_pos):
                self.selecionado = i
                return self.opcao_escolhida()
        return None