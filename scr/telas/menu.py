import pygame
from typing import List, Optional, Tuple
from constantes import Constantes
from componentes.button import Button

class Menu:
    def __init__(self, tela: pygame.Surface, fundo: pygame.Surface,
                 botoes: List[Button], fonte: pygame.font.Font) -> None:
        self.tela = tela
        self.fundo = fundo
        self.botoes = botoes
        self.selecionado: int = 0
        self.fonte = fonte

    def desenhar(self) -> None:
        self.tela.blit(self.fundo, (0, 0))

        for i, botao in enumerate(self.botoes):
            botao.desenhar(self.tela, i == self.selecionado)

    def mover_selecao(self, direcao: int) -> None:
        self.selecionado = (self.selecionado + direcao) % len(self.botoes)

    def opcao_selecionada(self) -> str:
        return self.botoes[self.selecionado].texto

    def verificar_clique(self, pos: Tuple[int, int]) -> Optional[str]:
        for botao in self.botoes:
            if botao.clicado(pos):
                return botao.texto
        
        return None