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
        
        # Atributos de combate
        self.dano: int = 10
        self.raio_ataque: int = 80
        self._ataque_cooldown: int = 1500  # Ataca a cada 1.5 segundos
        self._tempo_ultimo_ataque: int = 0
        self._dano_aplicado: bool = False

        self.velocidade: int = 2
        
        # Redimensiona as animações
        for acao, frames in self.animacoes.items():
            self.animacoes[acao] = [
                pygame.transform.scale(frame, (frame.get_width() * 2, frame.get_height() * 2)) 
                for frame in frames
            ]

        self.image = self.animacoes[self.acao][self.indice_frame]
        self.rect = self.image.get_rect(bottomleft=(x, y_chao))

    # Novo método que verifica se o esqueleto pode causar dano (similar ao do jogador)
    def pode_causar_dano(self) -> bool:
        """Retorna True uma única vez durante a animação de ataque."""
        # O dano é aplicado no frame 3 da animação 'atacar'
        if self.acao == 'atacar' and not self._dano_aplicado and self.indice_frame >= 3:
            self._dano_aplicado = True
            return True
        return False

    # A lógica de update foi refeita para incluir o ataque
    def update(self, rect_jogador: pygame.Rect) -> None:
        if not self.vivo:
            self.mudar_acao('morrer')
            super().update()
            return

        agora = pygame.time.get_ticks()
        distancia_x = self.rect.centerx - rect_jogador.centerx
        
        nova_acao = self.acao
        
        # Decide se deve atacar ou correr
        if abs(distancia_x) < self.raio_ataque:
            # Para de correr e se prepara para atacar
            self.velocidade = 0
            if agora - self._tempo_ultimo_ataque > self._ataque_cooldown:
                nova_acao = 'atacar'
                self._tempo_ultimo_ataque = agora
                self._dano_aplicado = False # Reseta a flag de dano a cada novo ataque
        else:
            # Volta a correr se o jogador se afastar
            self.velocidade = 2
            nova_acao = 'correr'

        # Se não está atacando, ele se move
        if nova_acao == 'correr':
            # Determina a direção
            if distancia_x > 0:
                self.direcao = -1 # Esquerda
            else:
                self.direcao = 1 # Direita
            
            self.rect.x += self.velocidade * self.direcao
        
        self.mudar_acao(nova_acao)
        super().update()