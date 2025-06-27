import pygame
from pygame import mixer
from typing import TYPE_CHECKING, List, Tuple

from constantes import Constantes
if TYPE_CHECKING:
    from game import Game


class ConfigScreen:
    def __init__(self, game: 'Game') -> None:
        self.game = game
        self.volume_musica: float = mixer.music.get_volume()
        self.volume_efeitos: float = 0.5
        self.fonte_grande: pygame.font.Font = pygame.font.Font(None, 75)
        self.fonte: pygame.font.Font = pygame.font.Font(None, 50)

        slider_width = Constantes.LARGURA * 0.4
        y_musica = Constantes.ALTURA * 0.4
        y_efeitos = Constantes.ALTURA * 0.6

        self.slider_musica_rect = pygame.Rect(0, 0, slider_width, 20)
        self.slider_musica_rect.center = (Constantes.LARGURA // 2, y_musica)

        self.slider_efeitos_rect = pygame.Rect(0, 0, slider_width, 20)
        self.slider_efeitos_rect.center = (Constantes.LARGURA // 2, y_efeitos)

        self.arrastando_musica: bool = False
        self.arrastando_efeitos: bool = False

    def desenhar(self, tela: pygame.Surface) -> None:
        tela.fill((40, 40, 40))

        titulo_surf = self.fonte_grande.render("Configurações", True, Constantes.COR_TEXTO)
        titulo_rect = titulo_surf.get_rect(center=(Constantes.LARGURA / 2, Constantes.ALTURA * 0.2))
        tela.blit(titulo_surf, titulo_rect)

        label_musica_surf = self.fonte.render("Música:", True, Constantes.COR_TEXTO)
        label_musica_rect = label_musica_surf.get_rect(midright=(self.slider_musica_rect.left - 30, self.slider_musica_rect.centery))
        tela.blit(label_musica_surf, label_musica_rect)
        
        pygame.draw.rect(tela, Constantes.COR_SLIDER, self.slider_musica_rect, border_radius=10)
        pos_circulo_musica: int = int(self.slider_musica_rect.x + self.slider_musica_rect.width * self.volume_musica)
        pygame.draw.circle(tela, (255, 0, 0), (pos_circulo_musica, self.slider_musica_rect.centery), 15)

        label_efeitos_surf = self.fonte.render("Efeitos:", True, Constantes.COR_TEXTO)
        label_efeitos_rect = label_efeitos_surf.get_rect(midright=(self.slider_efeitos_rect.left - 30, self.slider_efeitos_rect.centery))
        tela.blit(label_efeitos_surf, label_efeitos_rect)
        
        pygame.draw.rect(tela, Constantes.COR_SLIDER, self.slider_efeitos_rect, border_radius=10)
        pos_circulo_efeitos: int = int(self.slider_efeitos_rect.x + self.slider_efeitos_rect.width * self.volume_efeitos)
        pygame.draw.circle(tela, (0, 255, 0), (pos_circulo_efeitos, self.slider_efeitos_rect.centery), 15)

    def processar_eventos(self, eventos: List[pygame.event.Event]) -> None:
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    if self.slider_musica_rect.inflate(0, 40).collidepoint(evento.pos):
                        self.arrastando_musica = True
                        self.ajustar_volume(evento.pos)
                    elif self.slider_efeitos_rect.inflate(0, 40).collidepoint(evento.pos):
                        self.arrastando_efeitos = True
                        self.ajustar_volume(evento.pos)

            elif evento.type == pygame.MOUSEBUTTONUP:
                if evento.button == 1:
                    self.arrastando_musica = False
                    self.arrastando_efeitos = False
            elif evento.type == pygame.MOUSEMOTION:
                if self.arrastando_musica or self.arrastando_efeitos:
                    self.ajustar_volume(evento.pos)

    def ajustar_volume(self, pos: Tuple[int, int]) -> None:
        x, y = pos
        if self.arrastando_musica:
            novo_volume: float = (x - self.slider_musica_rect.x) / self.slider_musica_rect.width
            self.volume_musica = max(0.0, min(novo_volume, 1.0))
            mixer.music.set_volume(self.volume_musica)
        elif self.arrastando_efeitos:
            novo_volume = (x - self.slider_efeitos_rect.x) / self.slider_efeitos_rect.width
            self.volume_efeitos = max(0.0, min(novo_volume, 1.0))