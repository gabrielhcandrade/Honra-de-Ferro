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
        # CORREÇÃO: Lista de ações simplificada.
        acoes = ['parar', 'morrer']
        super().__init__(vida_maxima=vida, nome_entidade='dragao', asset_manager=asset_manager, acoes_animacao=acoes)
        
        self.rect = self.image.get_rect(topleft=(x, y))
        
        # Atributos de combate
        self.grupo_projeteis = grupo_projeteis
        self._ataque_cooldown: int = 2000  # Dispara a cada 2 segundos
        self._tempo_ultimo_ataque: int = pygame.time.get_ticks()

    # CORREÇÃO: Lógica de update totalmente refeita e simplificada.
    def update(self, rect_jogador: pygame.Rect) -> None:
        # Se não estiver vivo, executa a animação de morte e para.
        if not self.vivo:
            self.mudar_acao('morrer')
            super().update()
            return

        # A ação padrão é sempre 'parar'.
        self.mudar_acao('parar')
        
        # Lógica de disparo baseada apenas no tempo.
        agora = pygame.time.get_ticks()
        if agora - self._tempo_ultimo_ataque > self._ataque_cooldown:
            self._tempo_ultimo_ataque = agora
            
            # Cria e dispara a bola de fogo.
            origem_x = self.rect.midleft[0] + 40
            origem_y = self.rect.midleft[1] - 10
            origem_pos = (origem_x, origem_y)
            alvo_pos = rect_jogador.center
            
            bola = BolaDeFogo(origem_pos, alvo_pos, self.asset_manager)
            self.grupo_projeteis.add(bola)

        # Atualiza a animação (que será a de 'parar' em loop).
        super().update()
        
    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({
            "vida_maxima": self.vida_maxima,
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
        dragao.vida = data.get("vida", dragao.vida_maxima)
        dragao.acao = data.get("acao", "parar")
        dragao.indice_frame = data.get("indice_frame", 0)
        dragao.animar()
        return dragao