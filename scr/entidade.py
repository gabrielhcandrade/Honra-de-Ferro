import pygame
from typing import Dict, List, TYPE_CHECKING, Any
from dano import DanoPopup
from constantes import Constantes

if TYPE_CHECKING:
    from asset_manager import AssetManager

class Entidade(pygame.sprite.Sprite):
    def __init__(self, vida_maxima: int, nome_entidade: str, asset_manager: 'AssetManager', acoes_animacao: List[str]) -> None:
        super().__init__()
        self.vida_maxima: int = vida_maxima
        self._vida: int = vida_maxima
        self.nome_entidade = nome_entidade
        self.asset_manager = asset_manager
        
        self.animacoes: Dict[str, List[pygame.Surface]] = {}
        self.acao: str = acoes_animacao[0] if acoes_animacao else ''
        self.indice_frame: int = 0
        self.direcao = 1
        
        self.tempo_ultimo_frame: int = pygame.time.get_ticks()
        self.intervalo_animacao: int = 120
        
        self._carregar_animacoes(acoes_animacao)
        
        self.image = self.animacoes.get(self.acao, [pygame.Surface((50,50))])[0]
        self.rect = self.image.get_rect()

        # Grupo para gerenciar os pop-ups de dano da entidade
        self.grupo_popup_dano = pygame.sprite.Group()

    @property
    def vida(self) -> int:
        return self._vida

    @vida.setter
    def vida(self, valor: int) -> None:
        self._vida = max(0, min(valor, self.vida_maxima))
        if self._vida == 0 and self.acao != 'morrer':
            self.mudar_acao('morrer')
            self.indice_frame = 0 # Garante que a animação de morte comece do início

    @property
    def vivo(self) -> bool:
        return self._vida > 0

    def _carregar_animacoes(self, acoes: List[str]):
        for acao in acoes:
            self.animacoes[acao] = self.asset_manager.get_animacao(self.nome_entidade, acao)
            
    def mudar_acao(self, nova_acao: str):
        if self.acao != nova_acao:
            self.acao = nova_acao
            self.indice_frame = 0

    def animar(self) -> None:
        lista_frames = self.animacoes.get(self.acao)
        if not lista_frames:
            return

        agora = pygame.time.get_ticks()
        if agora - self.tempo_ultimo_frame > self.intervalo_animacao:
            self.tempo_ultimo_frame = agora
            self.indice_frame += 1
            
            if self.indice_frame >= len(lista_frames):
                if self.acao == 'morrer':
                    self.indice_frame = len(lista_frames) - 1
                    # A entidade para no último frame de morte, a lógica de remoção fica na batalha
                else:
                    self.indice_frame = 0
        
        imagem_base = lista_frames[self.indice_frame]
        self.image = pygame.transform.flip(imagem_base, self.direcao == -1, False)

    def receber_dano(self, quantidade: int):
        if self.vivo:
            self.vida -= quantidade
            popup = DanoPopup(str(quantidade), self.rect.center, Constantes.VERMELHO)
            self.grupo_popup_dano.add(popup)
    
    def curar(self, quantidade: int):
        if self.vivo:
            self.vida += quantidade
            popup = DanoPopup(f"+{quantidade}", self.rect.center, Constantes.VERDE)
            self.grupo_popup_dano.add(popup)


    def update(self, *args, **kwargs):
        self.animar()
        self.grupo_popup_dano.update()
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            'vida': self.vida,
            'x': self.rect.x,
            'y': self.rect.y,
            'acao': self.acao,
            'indice_frame': self.indice_frame,
            'direcao': self.direcao
        }
    
    def reset(self):
        self._vida = self.vida_maxima
        self.acao = 'parar'
        self.indice_frame = 0
        self.direcao = 1
        self.rect.topleft = (0, 0)
        self.grupo_popup_dano.empty()