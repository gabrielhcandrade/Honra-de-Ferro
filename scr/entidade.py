import pygame
from typing import Dict, List, TYPE_CHECKING, Any
from dano import DanoPopup
from constantes import Constantes

if TYPE_CHECKING:
    from asset_manager import AssetManager

class Entidade(pygame.sprite.Sprite):
    def __init__(self, vida_maxima: int, nome_entidade: str, asset_manager: 'AssetManager', acoes_animacao: List[str]) -> None:
        super().__init__()
        self._vida_maxima: int = vida_maxima
        self._vida: int = vida_maxima
        self._nome_entidade: str = nome_entidade
        self._asset_manager: 'AssetManager' = asset_manager
        
        self._animacoes: Dict[str, List[pygame.Surface]] = {}
        self._acao: str = acoes_animacao[0] if acoes_animacao else ''
        self._indice_frame: int = 0
        self._direcao: int = 1
        
        self._tempo_ultimo_frame: int = pygame.time.get_ticks()
        self._intervalo_animacao: int = 120
        
        self._carregar_animacoes(acoes_animacao)
        
        self.image: pygame.Surface = self._animacoes.get(self._acao, [pygame.Surface((50,50))])[0]
        self.rect: pygame.Rect = self.image.get_rect()

        self._grupo_popup_dano = pygame.sprite.Group()

    @property
    def vida(self) -> int:
        return self._vida

    @property
    def vivo(self) -> bool:
        return self._vida > 0
        
    def get_rect(self) -> pygame.Rect:
        return self.rect
        
    def get_direcao(self) -> int:
        return self._direcao

    def get_acao(self) -> str:
        return self._acao
        
    def get_indice_frame(self) -> int:
        return self._indice_frame
        
    def get_vida_maxima(self) -> int:
        return self._vida_maxima
        
    def get_grupo_popup_dano(self) -> pygame.sprite.Group:
        return self._grupo_popup_dano
        
    def get_animacoes(self) -> Dict[str, List[pygame.Surface]]:
        return self._animacoes

    @vida.setter
    def vida(self, valor: int) -> None:
        self._vida = max(0, min(valor, self._vida_maxima))
        if self._vida == 0 and self._acao != 'morrer':
            self.mudar_acao('morrer')
            self._indice_frame = 0 
            
    def set_direcao(self, valor: int) -> None:
        self._direcao = valor

    def set_acao(self, valor: str) -> None:
        self._acao = valor

    def set_indice_frame(self, valor: int) -> None:
        self._indice_frame = valor

    def _carregar_animacoes(self, acoes: List[str]):
        for acao in acoes:
            self._animacoes[acao] = self._asset_manager.get_animacao(self._nome_entidade, acao)
            
    def mudar_acao(self, nova_acao: str):
        if self._acao != nova_acao:
            self._acao = nova_acao
            self._indice_frame = 0

    def animar(self) -> None:
        lista_frames = self._animacoes.get(self._acao)
        if not lista_frames:
            return

        agora = pygame.time.get_ticks()
        if agora - self._tempo_ultimo_frame > self._intervalo_animacao:
            self._tempo_ultimo_frame = agora
            self._indice_frame += 1
            
            if self._indice_frame >= len(lista_frames):
                if self._acao == 'morrer':
                    self._indice_frame = len(lista_frames) - 1
                else:
                    self._indice_frame = 0
        
        imagem_base = lista_frames[self._indice_frame]
        self.image = pygame.transform.flip(imagem_base, self._direcao == -1, False)

    def receber_dano(self, quantidade: int):
        if self.vivo:
            self.vida -= quantidade
            popup = DanoPopup(str(quantidade), self.rect.center, Constantes.VERMELHO)
            self._grupo_popup_dano.add(popup)
    
    def curar(self, quantidade: int):
        if self.vivo:
            self.vida += quantidade
            popup = DanoPopup(f"+{quantidade}", self.rect.center, Constantes.VERDE)
            self._grupo_popup_dano.add(popup)

    def update(self, *args, **kwargs):
        self.animar()
        self._grupo_popup_dano.update()
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            'vida': self.vida,
            'x': self.rect.x,
            'y': self.rect.y,
            'acao': self._acao,
            'indice_frame': self._indice_frame,
            'direcao': self._direcao
        }
    
    def reset(self):
        self._vida = self._vida_maxima
        self._acao = 'parar'
        self._indice_frame = 0
        self._direcao = 1
    #    self.rect.topleft = (0, 0)
        self._grupo_popup_dano.empty()