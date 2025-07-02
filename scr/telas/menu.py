import pygame
from typing import List, Optional, Tuple
from constantes import Constantes
from componentes.button import Button

class Menu:
    def __init__(self, tela: pygame.Surface, fundo: pygame.Surface,
                 botoes: List[Button], fonte: pygame.font.Font) -> None:
        self._tela = tela
        self._fundo = fundo
        self._botoes = botoes
        self._selecionado: int = 0
        self._fonte = fonte

    def desenhar(self) -> None:
        self._tela.blit(self._fundo, (0, 0))
        for i, botao in enumerate(self._botoes):
            botao.desenhar(self._tela, i == self._selecionado)

    def mover_selecao(self, direcao: int) -> None:
        self._selecionado = (self._selecionado + direcao) % len(self._botoes)

    def opcao_selecionada(self) -> str:
        return self._botoes[self._selecionado].get_texto()

    def verificar_clique(self, pos: Tuple[int, int]) -> Optional[str]:
        for botao in self._botoes:
            if botao.clicado(pos):
                return botao.get_texto()
        return None