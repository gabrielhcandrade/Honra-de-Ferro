import pygame
from typing import Optional, Tuple

from constantes import Constantes


class Button:
    def __init__(self, texto: str, posicao: Tuple[int, int], fonte: pygame.font.Font,
                 largura_extra: int = 60, altura_extra: int = 40, imagem: Optional[pygame.Surface] = None) -> None:
        self.texto = texto
        self.posicao = posicao
        self.fonte = fonte
        self.largura_extra = largura_extra
        self.altura_extra = altura_extra
        self.imagem = imagem
        self.ret: Optional[pygame.Rect] = None

    def desenhar(self, tela: pygame.Surface, selecionado: bool = False) -> None:
        if self.imagem:
            self.ret = self.imagem.get_rect(center=self.posicao)
            tela.blit(self.imagem, self.ret)
        else:
            cor: Tuple[int, int, int] = Constantes.COR_SELECIONADA if selecionado else Constantes.COR_TEXTO
            texto_renderizado: pygame.Surface = self.fonte.render(self.texto, True, cor)
            self.ret = texto_renderizado.get_rect(center=self.posicao)
            pygame.draw.rect(tela, Constantes.COR_BOTAO, self.ret.inflate(self.largura_extra, self.altura_extra))
            tela.blit(texto_renderizado, self.ret)

    def clicado(self, mouse_pos: Tuple[int, int]) -> bool:
        return self.ret is not None and self.ret.collidepoint(mouse_pos)