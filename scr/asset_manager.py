import pygame
import os
from constantes import Constantes
from typing import Optional

class AssetManager:
    def __init__(self) -> None:
        self._animations: dict[str, dict[str, list[pygame.Surface]]] = {}
        self._images: dict[str, pygame.Surface] = {}
        self._sounds: dict[str, pygame.mixer.Sound] = {}

        self._carregar_fontes()
        self._carregar_recursos()

    def _carregar_fontes(self):
        caminho_fonte = os.path.join('../assets/fontes/OldLondon.ttf')
        try:
            self._fonte_30 = pygame.font.Font(caminho_fonte, 30)
            self._fonte_50 = pygame.font.Font(caminho_fonte, 50)
            self._fonte_100 = pygame.font.Font(caminho_fonte, 100)
        except pygame.error as e:
            print(f"Erro ao carregar a fonte '{caminho_fonte}': {e}. Usando fonte padrão.")
            self._fonte_30 = pygame.font.SysFont(None, 30)
            self._fonte_50 = pygame.font.SysFont(None, 50)
            self._fonte_100 = pygame.font.SysFont(None, 100)

    @property
    def fonte_30(self): return self._fonte_30

    @property
    def fonte_50(self): return self._fonte_50

    @property
    def fonte_100(self): return self._fonte_100

    def _criar_placeholder(self) -> pygame.Surface:
        placeholder = pygame.Surface((50, 50))
        placeholder.fill(Constantes.ROSA)
        return placeholder

    def _carregar_recursos(self):
        self._carregar_imagens_estaticas()
        self._carregar_animacoes()
        self._carregar_sons()

    def _carregar_imagens_estaticas(self):
        imagens = {
            'fundo': '../assets/img/fundo.png',
            'fundobatalha': '../assets/img/fundobatalha.png',
            'fundo2': '../assets/img/fundo2.png',
            'pocao': '../assets/img/potion.png',
            'bola_de_fogo': '../assets/img/fireball.png'
        }
        for chave, caminho in imagens.items():
            try:
                self._images[chave] = pygame.image.load(caminho).convert_alpha()
            except Exception as e:
                print(f"Erro ao carregar imagem '{chave}': {e}")
                self._images[chave] = self._criar_placeholder()

    def _carregar_sons(self):
        sons = {
            'espada': '../assets/sons/espada.mp3',
            'poder': '../assets/sons/poder.mp3'
        }
        for chave, caminho in sons.items():
            try:
                self._sounds[chave] = pygame.mixer.Sound(caminho)
            except Exception as e:
                print(f"Erro ao carregar som '{chave}': {e}")

    def _carregar_animacoes(self):
        self._carregar_pasta_animacao('guerreiro', ['parar', 'correr', 'atacar', 'pular', 'morrer', 'defender'])
        self._carregar_pasta_animacao('inimigo', ['correr', 'atacar', 'morrer'])
        
        # CORREÇÃO: Dragão agora só precisa das animações 'parar' e 'morrer'.
        self._carregar_pasta_animacao('dragao', ['parar', 'morrer'], scale_factor=3)

    def _carregar_pasta_animacao(self, nome_personagem, lista_acoes, scale_factor=1):
        if nome_personagem not in self._animations:
            self._animations[nome_personagem] = {}

        for acao in lista_acoes:
            pasta_acao = f'../assets/img/{nome_personagem}/{acao}'
            frames = self._carregar_frames_de_pasta(pasta_acao)

            if scale_factor != 1 and frames and frames[0].get_width() > 1:
                frames = [
                    pygame.transform.scale(f, (
                        int(f.get_width() * scale_factor),
                        int(f.get_height() * scale_factor)
                    )) for f in frames
                ]

            self._animations[nome_personagem][acao] = frames

    def _carregar_frames_de_pasta(self, caminho_pasta: str) -> list[pygame.Surface]:
        frames = []
        if not os.path.exists(caminho_pasta):
            print(f"AVISO: Pasta de animação não encontrada em '{caminho_pasta}'")
            return [self._criar_placeholder()]

        try:
            arquivos = sorted(os.listdir(caminho_pasta), key=lambda x: int(x.split('.')[0]))
            for nome in arquivos:
                caminho = os.path.join(caminho_pasta, nome)
                if os.path.isfile(caminho):
                    imagem = pygame.image.load(caminho).convert_alpha()
                    frames.append(imagem)
        except Exception as e:
            print(f"Erro ao carregar frames de '{caminho_pasta}': {e}")
            return [self._criar_placeholder()]

        if not frames:
            print(f"AVISO: Nenhum frame encontrado em '{caminho_pasta}'")
            return [self._criar_placeholder()]
        return frames

    def get_animacao(self, personagem: str, acao: str) -> list[pygame.Surface]:
        return self._animations.get(personagem, {}).get(acao, [self._criar_placeholder()])

    def get_imagem(self, nome_imagem: str) -> pygame.Surface:
        return self._images.get(nome_imagem, self._criar_placeholder())

    def get_som(self, nome_som: str) -> Optional[pygame.mixer.Sound]:
        return self._sounds.get(nome_som)