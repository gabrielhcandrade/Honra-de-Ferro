import pygame
from pygame import mixer
from typing import TYPE_CHECKING, List, Tuple

from constantes import Constantes
if TYPE_CHECKING:
    from game import Game

class ConfigScreen:
    def __init__(self, game: 'Game') -> None:
        self._game = game
        self._volume_musica: float = mixer.music.get_volume()
        self._volume_efeitos: float = 0.5
        self._fonte_grande: pygame.font.Font = pygame.font.Font(None, 75)
        self._fonte: pygame.font.Font = pygame.font.Font(None, 50)

        slider_width = Constantes.LARGURA * 0.4
        y_musica = Constantes.ALTURA * 0.4
        y_efeitos = Constantes.ALTURA * 0.6

        self._slider_musica_rect = pygame.Rect(0, 0, slider_width, 20)
        self._slider_musica_rect.center = (Constantes.LARGURA // 2, y_musica)

        self._slider_efeitos_rect = pygame.Rect(0, 0, slider_width, 20)
        self._slider_efeitos_rect.center = (Constantes.LARGURA // 2, y_efeitos)

        self._arrastando_musica: bool = False
        self._arrastando_efeitos: bool = False

    def get_volume_efeitos(self) -> float:
        return self._volume_efeitos

    def desenhar(self, tela: pygame.Surface) -> None:
        tela.fill((40, 40, 40))

        titulo_surf = self._fonte_grande.render("Configurações", True, Constantes.COR_TEXTO)
        titulo_rect = titulo_surf.get_rect(center=(Constantes.LARGURA / 2, Constantes.ALTURA * 0.2))
        tela.blit(titulo_surf, titulo_rect)

        label_musica_surf = self._fonte.render("Música:", True, Constantes.COR_TEXTO)
        label_musica_rect = label_musica_surf.get_rect(midright=(self._slider_musica_rect.left - 30, self._slider_musica_rect.centery))
        tela.blit(label_musica_surf, label_musica_rect)
        
        pygame.draw.rect(tela, Constantes.COR_SLIDER, self._slider_musica_rect, border_radius=10)
        pos_circulo_musica: int = int(self._slider_musica_rect.x + self._slider_musica_rect.width * self._volume_musica)
        pygame.draw.circle(tela, (255, 0, 0), (pos_circulo_musica, self._slider_musica_rect.centery), 15)

        label_efeitos_surf = self._fonte.render("Efeitos:", True, Constantes.COR_TEXTO)
        label_efeitos_rect = label_efeitos_surf.get_rect(midright=(self._slider_efeitos_rect.left - 30, self._slider_efeitos_rect.centery))
        tela.blit(label_efeitos_surf, label_efeitos_rect)
        
        pygame.draw.rect(tela, Constantes.COR_SLIDER, self._slider_efeitos_rect, border_radius=10)
        pos_circulo_efeitos: int = int(self._slider_efeitos_rect.x + self._slider_efeitos_rect.width * self._volume_efeitos)
        pygame.draw.circle(tela, (0, 255, 0), (pos_circulo_efeitos, self._slider_efeitos_rect.centery), 15)

    def processar_eventos(self, eventos: List[pygame.event.Event]) -> None:
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    if self._slider_musica_rect.inflate(0, 40).collidepoint(evento.pos):
                        self._arrastando_musica = True
                        self.ajustar_volume(evento.pos)
                    elif self._slider_efeitos_rect.inflate(0, 40).collidepoint(evento.pos):
                        self._arrastando_efeitos = True
                        self.ajustar_volume(evento.pos)

            elif evento.type == pygame.MOUSEBUTTONUP:
                if evento.button == 1:
                    self._arrastando_musica = False
                    self._arrastando_efeitos = False
            elif evento.type == pygame.MOUSEMOTION:
                if self._arrastando_musica or self._arrastando_efeitos:
                    self.ajustar_volume(evento.pos)

    def ajustar_volume(self, pos: Tuple[int, int]) -> None:
        x, y = pos
        if self._arrastando_musica:
            novo_volume: float = (x - self._slider_musica_rect.x) / self._slider_musica_rect.width
            self._volume_musica = max(0.0, min(novo_volume, 1.0))
            mixer.music.set_volume(self._volume_musica)
        elif self._arrastando_efeitos:
            novo_volume = (x - self._slider_efeitos_rect.x) / self._slider_efeitos_rect.width
            self._volume_efeitos = max(0.0, min(novo_volume, 1.0))