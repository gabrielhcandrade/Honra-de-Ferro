import pygame
import math
from entidade import Entidade
from asset_manager import AssetManager
from bola_de_fogo import BolaDeFogo
from constantes import Constantes
from typing import Optional

class Dragao(Entidade):
    def __init__(
        self,
        x: int,
        y: int,
        asset_manager: AssetManager,
        grupo_projeteis: pygame.sprite.Group,
        vida: int = 500
    ) -> None:
        acoes = ['parar', 'morrer']
        super().__init__(vida_maxima=vida, nome_entidade='dragao', asset_manager=asset_manager, acoes_animacao=acoes)
        
        self.rect = self.image.get_rect(topleft=(x, y))
        
        self._grupo_projeteis = grupo_projeteis
        self._ataque_cooldown: int = 2000 
        self._tempo_ultimo_ataque: int = pygame.time.get_ticks()

    def update(self, rect_jogador: pygame.Rect) -> None:
        if not self.vivo:
            self.mudar_acao('morrer')
            super().update()
            return

        self.mudar_acao('parar')
        
        agora = pygame.time.get_ticks()
        if agora - self._tempo_ultimo_ataque > self._ataque_cooldown:
            self._tempo_ultimo_ataque = agora
            
            origem_x = self.rect.midleft[0] + 40
            origem_y = self.rect.midleft[1] - 10
            origem_pos = (origem_x, origem_y)
            alvo_pos = rect_jogador.center
            
            bola = BolaDeFogo(origem_pos, alvo_pos, self._asset_manager)
            self._grupo_projeteis.add(bola)

        super().update()
        
    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({
            "vida_maxima": self.get_vida_maxima(),
        })
        return data

    @classmethod
    def from_dict(cls, data: dict, asset_manager: AssetManager, grupo_projeteis: pygame.sprite.Group) -> 'Dragao':
        dragao = cls(
            x=data.get("x", 1200),
            y=data.get("y", 400),
            asset_manager=asset_manager,
            grupo_projeteis=grupo_projeteis,
            vida=data.get("vida_maxima", 500)
        )
        dragao.vida = data.get("vida", dragao.get_vida_maxima())
        dragao.set_acao(data.get("acao", "parar"))
        dragao.set_indice_frame(data.get("indice_frame", 0))
        dragao.animar()
        return dragao

    @property
    def get_grupo_projeteis(self) -> pygame.sprite.Group:
        return self._grupo_projeteis

    def set_grupo_projeteis(self, grupo: pygame.sprite.Group) -> None:
        self._grupo_projeteis = grupo

    @property
    def get_ataque_cooldown(self) -> int:
        return self._ataque_cooldown

    def set_ataque_cooldown(self, cooldown: int) -> None:
        self._ataque_cooldown = cooldown

    @property
    def get_tempo_ultimo_ataque(self) -> int:
        return self._tempo_ultimo_ataque

    def set_tempo_ultimo_ataque(self, tempo: int) -> None:
        self._tempo_ultimo_ataque = tempo