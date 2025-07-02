import pygame
from typing import Optional, Tuple
from constantes import Constantes

class Button:
    def __init__(self, texto: str, posicao: Tuple[int, int], fonte: pygame.font.Font,
                 largura_extra: int = 60, altura_extra: int = 40, imagem: Optional[pygame.Surface] = None) -> None:
        self._texto = texto
        self._posicao = posicao
        self._fonte = fonte
        self._largura_extra = largura_extra
        self._altura_extra = altura_extra
        self._imagem = imagem
        self._ret: Optional[pygame.Rect] = None

    def get_texto(self) -> str:
        return self._texto

    def desenhar(self, tela: pygame.Surface, selecionado: bool = False) -> None:
        if self._imagem:
            self._ret = self._imagem.get_rect(center=self._posicao)
            tela.blit(self._imagem, self._ret)
        else:
            cor: Tuple[int, int, int] = Constantes.COR_SELECIONADA if selecionado else Constantes.COR_TEXTO
            texto_renderizado: pygame.Surface = self._fonte.render(self._texto, True, cor)
            self._ret = texto_renderizado.get_rect(center=self._posicao)
            pygame.draw.rect(tela, Constantes.COR_BOTAO, self._ret.inflate(self._largura_extra, self._altura_extra))
            tela.blit(texto_renderizado, self._ret)

    def clicado(self, mouse_pos: Tuple[int, int]) -> bool:
        return self._ret is not None and self._ret.collidepoint(mouse_pos)