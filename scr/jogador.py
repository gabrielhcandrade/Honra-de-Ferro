import pygame
from typing import Dict, Any
from entidade import Entidade
from asset_manager import AssetManager
from constantes import Constantes

class Jogador(Entidade):
    def __init__(
        self,
        asset_manager: AssetManager,
        x: int = 100,
        y_chao: int = 550,
        velocidade: int = 5,
        vida: int = 200
    ) -> None:
        acoes = ['parar', 'correr', 'pular', 'atacar', 'morrer', 'defender']
        super().__init__(vida_maxima=vida, nome_entidade='guerreiro', asset_manager=asset_manager, acoes_animacao=acoes)

        self._y_chao = y_chao
        self._velocidade = velocidade
        self._pulando = False
        self._vel_y = 0
        self._num_pocoes = 3
        self._defendendo = False
        self._atacando = False
        self._dano_aplicado = False
        self._tempo_ataque = 0
        self._ataque_cooldown = 400
        self._direcao = 1

        self.is_dashing = False
        self.dash_speed = 25
        self.dash_duration = 150
        self.dash_end_time = 0
        self.dash_cooldown = 3000
        self.last_dash_time = -self.dash_cooldown

        for acao in self.animacoes:
            self.animacoes[acao] = [
                pygame.transform.scale(frame, (frame.get_width() * 2, frame.get_height() * 2))
                for frame in self.animacoes[acao]
            ]

        self.image = self.animacoes[self.acao][self.indice_frame]
        self.rect = self.image.get_rect(bottomleft=(x, self._y_chao))


    @property
    def y_chao(self) -> int:
        return self._y_chao

    @y_chao.setter
    def y_chao(self, valor: int):
        self._y_chao = valor
        self.rect.bottom = valor

    @property
    def direcao(self) -> int:
        return self._direcao

    @direcao.setter
    def direcao(self, valor: int):
        if valor not in [-1, 1]:
            raise ValueError("Direção deve ser -1 (esquerda) ou 1 (direita)")
        self._direcao = valor

    @property
    def num_pocoes(self) -> int:
        return self._num_pocoes

    @property
    def defendendo(self) -> bool:
        return self._defendendo

    @property
    def atacando(self) -> bool:
        return self._atacando

    def reset(self) -> None:
        super().reset()
        self.rect.bottomleft = (100, self._y_chao)
        self._pulando = False
        self._vel_y = 0
        self._num_pocoes = 3
        self.last_dash_time = -self.dash_cooldown

    def aplicar_gravidade(self) -> None:
        self._vel_y += Constantes.GRAVIDADE
        if self._vel_y > Constantes.VEL_MAX_QUEDA:
            self._vel_y = Constantes.VEL_MAX_QUEDA

        self.rect.y += self._vel_y

        if self.rect.bottom >= self._y_chao:
            self.rect.bottom = self._y_chao
            self._pulando = False
            self._vel_y = 0

    def processar_movimento(self, teclas: pygame.key.ScancodeWrapper, volume_efeitos: float) -> None:
        dx = 0
        agora = pygame.time.get_ticks()

        if self.is_dashing:
            if agora > self.dash_end_time:
                self.is_dashing = False
            else:
                self.rect.x += self.dash_speed * self.direcao
                self.rect.clamp_ip(pygame.Rect(0, 0, Constantes.LARGURA, Constantes.ALTURA))
                return

        if self._atacando and agora - self._tempo_ataque > self._ataque_cooldown:
            self._atacando = False

        if self._atacando or not self.vivo:
            return

        self._defendendo = False

        if teclas[pygame.K_LEFT]:
            dx = -self._velocidade
            self.direcao = -1
        elif teclas[pygame.K_RIGHT]:
            dx = self._velocidade
            self.direcao = 1

        if teclas[pygame.K_UP] and not self._pulando:
            self._pulando = True
            self._vel_y = -20
        
        if teclas[pygame.K_LSHIFT] and not self.is_dashing:
            if agora - self.last_dash_time > self.dash_cooldown:
                self.is_dashing = True
                self.last_dash_time = agora
                self.dash_end_time = agora + self.dash_duration
                
                # CORREÇÃO: Toca o som de 'poder' ao usar a investida.
                som_poder = self.asset_manager.get_som('poder')
                if som_poder:
                    som_poder.set_volume(volume_efeitos)
                    som_poder.play()
        
        if teclas[pygame.K_SPACE] and not self._atacando:
            self._atacando = True
            self._dano_aplicado = False
            self._tempo_ataque = agora
            
            som_espada = self.asset_manager.get_som('espada')
            if som_espada:
                som_espada.set_volume(volume_efeitos)
                som_espada.play()

        if teclas[pygame.K_e]:
            self._defendendo = True

        if teclas[pygame.K_h] and self._num_pocoes > 0:
            self.usar_pocao()

        self.rect.x += dx
        self.rect.clamp_ip(pygame.Rect(0, 0, Constantes.LARGURA, Constantes.ALTURA))

    def update(self, teclas: pygame.key.ScancodeWrapper, volume_efeitos: float = 0.5, *args) -> None:
        if not self.vivo:
            self.mudar_acao('morrer')
            super().update()
            return

        self.processar_movimento(teclas, volume_efeitos)
        self.aplicar_gravidade()

        if self.is_dashing:
             nova_acao = 'correr'
        elif self._atacando:
            nova_acao = 'atacar'
        elif self._defendendo:
            nova_acao = 'defender'
        elif self._pulando:
            nova_acao = 'pular'
        elif teclas[pygame.K_LEFT] or teclas[pygame.K_RIGHT]:
            nova_acao = 'correr'
        else:
            nova_acao = 'parar'

        self.mudar_acao(nova_acao)
        super().update()

    def pode_causar_dano(self) -> bool:
        if self._atacando and not self._dano_aplicado and self.indice_frame > 1:
            self._dano_aplicado = True
            return True
        return False

    def coletar_pocao(self) -> None:
        self._num_pocoes += 1

    def usar_pocao(self) -> None:
        self.curar(50)
        self._num_pocoes -= 1

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "num_pocoes": self._num_pocoes,
            "y_chao": self._y_chao,
            "vida_maxima": self.vida_maxima,
            "last_dash_time": self.last_dash_time
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any], asset_manager: AssetManager) -> 'Jogador':
        y_chao = data.get("y_chao", 550)
        vida_maxima = data.get("vida_maxima", 200)
        
        jogador = cls(asset_manager, y_chao=y_chao, vida=vida_maxima)
        
        jogador.vida = data.get("vida", vida_maxima)
        jogador.rect.x = data.get("x", 100)
        jogador.rect.y = data.get("y", y_chao - jogador.rect.height)
        jogador.acao = data.get("acao", "parar")
        jogador.indice_frame = data.get("indice_frame", 0)
        jogador.direcao = data.get("direcao", 1)
        
        jogador._num_pocoes = data.get("num_pocoes", 3)
        jogador.last_dash_time = data.get("last_dash_time", -jogador.dash_cooldown)

        jogador.animar()
        
        return jogador