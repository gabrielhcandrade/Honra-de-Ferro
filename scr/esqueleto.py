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
        
        self._dano: int = 10
        self._raio_ataque: int = 80
        self._ataque_cooldown: int = 1500  
        self._tempo_ultimo_ataque: int = 0
        self._dano_aplicado: bool = False
        self._velocidade: int = 2
        
        self._animacoes = self.get_animacoes()
        for acao, frames in self._animacoes.items():
            self._animacoes[acao] = [
                pygame.transform.scale(frame, (frame.get_width() * 2, frame.get_height() * 2)) 
                for frame in frames
            ]

        self.image = self._animacoes[self.get_acao()][self.get_indice_frame()]
        self.rect = self.image.get_rect(bottomleft=(x, y_chao))

    def get_dano(self) -> int:
        return self._dano

    def pode_causar_dano(self) -> bool:
        if self.get_acao() == 'atacar' and not self._dano_aplicado and self.get_indice_frame() >= 3:
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
        
        nova_acao = self.get_acao()
        
        if abs(distancia_x) < self._raio_ataque:
            self._velocidade = 0
            if agora - self._tempo_ultimo_ataque > self._ataque_cooldown:
                nova_acao = 'atacar'
                self._tempo_ultimo_ataque = agora
                self._dano_aplicado = False 
        else:
            self._velocidade = 2
            nova_acao = 'correr'

        if nova_acao == 'correr':
            if distancia_x > 0:
                self.set_direcao(-1) 
            else:
                self.set_direcao(1) 
            
            self.rect.x += self._velocidade * self.get_direcao()
        
        self.mudar_acao(nova_acao)
        super().update()