import pygame
from entidade import Entidade
from asset_manager import AssetManager

class Esqueleto(Entidade):
    def __init__(
        self,
        x: int,
        y_chao: int,
        asset_manager: AssetManager,
        vida: int = 100
    ) -> None:
        acoes = ['correr', 'atacar', 'morrer']
        super().__init__(vida_maxima=vida, nome_entidade='inimigo', asset_manager=asset_manager, acoes_animacao=acoes)
        
        self.dano: int = 10
        self.raio_ataque: int = 80
        self._ataque_cooldown: int = 1500  
        self._tempo_ultimo_ataque: int = 0
        self._dano_aplicado: bool = False

        self.velocidade: int = 2
        
        for acao, frames in self.animacoes.items():
            self.animacoes[acao] = [
                pygame.transform.scale(frame, (frame.get_width() * 2, frame.get_height() * 2)) 
                for frame in frames
            ]

        self.image = self.animacoes[self.acao][self.indice_frame]
        self.rect = self.image.get_rect(bottomleft=(x, y_chao))

    def pode_causar_dano(self) -> bool:
        if self.acao == 'atacar' and not self._dano_aplicado and self.indice_frame >= 3:
            self._dano_aplicado = True
            return True
        return False

    def update(self, rect_jogador: pygame.Rect) -> None:
        if not self.vivo:
            self.mudar_acao('morrer')
            super().update()
            return

        agora = pygame.time.get_ticks()
        distancia_x = self.rect.centerx - rect_jogador.centerx
        
        nova_acao = self.acao
        
        if abs(distancia_x) < self.raio_ataque:
            self.velocidade = 0
            if agora - self._tempo_ultimo_ataque > self._ataque_cooldown:
                nova_acao = 'atacar'
                self._tempo_ultimo_ataque = agora
                self._dano_aplicado = False 
        else:
            self.velocidade = 2
            nova_acao = 'correr'

        if nova_acao == 'correr':
            if distancia_x > 0:
                self.direcao = -1 
            else:
                self.direcao = 1 
            
            self.rect.x += self.velocidade * self.direcao
        
        self.mudar_acao(nova_acao)
        super().update()