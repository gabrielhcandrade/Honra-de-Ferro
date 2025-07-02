import pygame
import sys
from pygame import mixer
import json
from typing import Optional, List
import os

from constantes import Constantes
from componentes.button import Button
from batalha_dragao import BatalhaDragao
from telas.game_over_screen import GameOverScreen
from telas.config_screen import ConfigScreen
from componentes.ranking_manager import RankingManager
from jogador_ranking import JogadorRanking
from nome_jogador import NomeJogador
from telas.menu import Menu
from telas.menu2 import Menu2
from telas.tela_ranking_pygame import TelaRankingPygame
from asset_manager import AssetManager


class Game:
    def __init__(self) -> None:
        pygame.init()
        mixer.init()

        self._fullscreen: bool = False
        self._tela: pygame.Surface = pygame.display.set_mode(
            (Constantes.LARGURA, Constantes.ALTURA))
        pygame.display.set_caption("Honra de Ferro")

        self._asset_manager = AssetManager()

        self._fundo = self._asset_manager.get_imagem('fundo')
        self._fundo = pygame.transform.scale(self._fundo, (Constantes.LARGURA, Constantes.ALTURA))
        
        self._fundo2 = self._asset_manager.get_imagem('fundo2')
        self._fundo2 = pygame.transform.scale(self._fundo, (Constantes.LARGURA, Constantes.ALTURA))


        try:
            mixer.music.load("../assets/sons/abertura.mp3")
            mixer.music.set_volume(0.1)
            mixer.music.play(-1)
        except pygame.error as e:
            print(f"Erro ao carregar ou tocar abertura.mp3: {e}")

        self._fonte = self._asset_manager.fonte_50
        self._fonte_titulo = self._asset_manager.fonte_100

        self._titulo_texto = self._fonte_titulo.render(
            "Honra de Ferro", True, Constantes.PRETO)
        self._titulo_rect = self._titulo_texto.get_rect(
            center=(Constantes.LARGURA // 2, 220))

        botoes: List[Button] = [
            Button("Jogar", (Constantes.LARGURA // 2, 360), self._fonte),
            Button("Score", (Constantes.LARGURA // 2, 470), self._fonte),
            Button("Configurações", (Constantes.LARGURA // 2, 580), self._fonte),
            Button("Sobre", (Constantes.LARGURA // 2, 690), self._fonte),
            Button("Sair", (Constantes.LARGURA // 2, 800), self._fonte),
        ]

        self._estado: str = "menu"
        self._nome_jogador_atual: Optional[str] = None
        self._pontos_finais: int = 0

        self._ranking_manager: RankingManager = RankingManager()
        self._menu: Menu = Menu(self._tela, self._fundo, botoes, self._fonte)
        self._config: ConfigScreen = ConfigScreen(self)
        self._menu2: Menu2 = Menu2(self._tela, self._asset_manager)
        self._nome_jogador: NomeJogador = NomeJogador(self._ranking_manager)
        self._batalha: BatalhaDragao = BatalhaDragao(self, self._tela, self._asset_manager)
        self._game_over_screen: GameOverScreen = GameOverScreen(self._tela)
        self._tela_ranking_pygame: TelaRankingPygame = TelaRankingPygame(self._tela, self._ranking_manager)

        self._submenu_jogar_opcoes: List[Button] = []
        self._submenu_jogar_selecionado: int = 0
        caminho_save = "../assets/ranking/save_game.json"
        y_inicial_submenu = Constantes.ALTURA // 2 - 100
        espacamento_submenu = 110

        if os.path.exists(caminho_save):
            self._submenu_jogar_opcoes.append(
                Button("Continuar", (Constantes.LARGURA // 2, y_inicial_submenu), self._fonte))
            self._submenu_jogar_opcoes.append(
                Button("Novo Jogo", (Constantes.LARGURA // 2, y_inicial_submenu + espacamento_submenu), self._fonte))
        else:
            self._submenu_jogar_opcoes.append(
                Button("Novo Jogo", (Constantes.LARGURA // 2, y_inicial_submenu), self._fonte))

    def get_tela(self) -> pygame.Surface:
        return self._tela

    def get_estado(self) -> str:
        return self._estado

    def set_estado(self, estado: str) -> None:
        self._estado = estado

    def get_config_screen(self) -> 'ConfigScreen':
        return self._config

    def executar(self) -> None:
        clock: pygame.time.Clock = pygame.time.Clock()
        rodando: bool = True

        while rodando:
            eventos: List[pygame.event.Event] = pygame.event.get()

            for evento in eventos:
                if evento.type == pygame.QUIT:
                    rodando = False

                if self._estado == "menu":
                    if evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_UP: self._menu.mover_selecao(-1)
                        elif evento.key == pygame.K_DOWN: self._menu.mover_selecao(1)
                        elif evento.key == pygame.K_RETURN: rodando = self.processar_escolha_menu(self._menu.opcao_selecionada())
                    elif evento.type == pygame.MOUSEBUTTONDOWN:
                        escolha_mouse = self._menu.verificar_clique(evento.pos)
                        if escolha_mouse: rodando = self.processar_escolha_menu(escolha_mouse)
                
                elif self._estado == "menu_jogar":
                    if evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_ESCAPE: self._estado = "menu"
                        elif evento.key == pygame.K_UP: self._submenu_jogar_selecionado = (self._submenu_jogar_selecionado - 1) % len(self._submenu_jogar_opcoes)
                        elif evento.key == pygame.K_DOWN: self._submenu_jogar_selecionado = (self._submenu_jogar_selecionado + 1) % len(self._submenu_jogar_opcoes)
                        elif evento.key == pygame.K_RETURN:
                            escolha = self._submenu_jogar_opcoes[self._submenu_jogar_selecionado].get_texto()
                            self.processar_escolha_submenu(escolha)
                    elif evento.type == pygame.MOUSEBUTTONDOWN:
                        for i, botao in enumerate(self._submenu_jogar_opcoes):
                            if botao.clicado(evento.pos):
                                self._submenu_jogar_selecionado = i
                                escolha = botao.get_texto()
                                self.processar_escolha_submenu(escolha)

                elif self._estado == "jogar":
                    if evento.type == pygame.KEYDOWN:
                        resultado = self._nome_jogador.processar_evento(evento)
                        if resultado == "confirmado":
                            self._nome_jogador_atual = self._nome_jogador.get_nome()
                            self._estado = "batalha"
                            self._batalha.reset_batalha()
                            self.salvar_progresso_jogo()
                        elif resultado == "voltar": self._estado = "menu"

                elif self._estado in ["ranking", "config", "menu2"]:
                    if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE: self._estado = "menu"
                
                elif self._estado == "batalha":
                    if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                        self.mostrar_menu_pausa()

                elif self._estado == "game_over":
                    if evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_UP: self._game_over_screen.mover_selecao(-1)
                        elif evento.key == pygame.K_DOWN: self._game_over_screen.mover_selecao(1)
                        elif evento.key == pygame.K_RETURN: rodando = self.processar_escolha_game_over(self._game_over_screen.opcao_escolhida())
                    elif evento.type == pygame.MOUSEBUTTONDOWN:
                        escolha_mouse = self._game_over_screen.verificar_clique(evento.pos)
                        if escolha_mouse: rodando = self.processar_escolha_game_over(escolha_mouse)

            if self._estado == "batalha":
                resultado = self._batalha.atualizar(self._config.get_volume_efeitos())
                if resultado:
                    self._pontos_finais = self._batalha.get_pontuacao_final()
                    if resultado == "Vitória":
                        self._adicionar_ao_ranking(self._pontos_finais)
                        self._estado = "vitória"
                    else:
                        self._estado = "game_over"
            
            if self._estado == "config":
                self._config.processar_eventos(eventos)

            self._tela.fill(Constantes.PRETO)
            if self._estado == "menu":
                self._menu.desenhar()
                self._tela.blit(self._titulo_texto, self._titulo_rect)
            elif self._estado == "menu_jogar":
                self._tela.fill(Constantes.PRETO)
                for i, botao in enumerate(self._submenu_jogar_opcoes):
                    selecionado = (i == self._submenu_jogar_selecionado)
                    botao.desenhar(self._tela, selecionado)
            elif self._estado == "config":
                self._config.desenhar(self._tela)
            elif self._estado == "menu2":
                self._menu2.desenhar()
            elif self._estado == "jogar":
                self._nome_jogador.desenhar(self._tela)
            elif self._estado == "batalha":
                self._batalha.desenhar()
            elif self._estado == "game_over":
                self._game_over_screen.desenhar()
            elif self._estado == "ranking":
                self._tela_ranking_pygame.desenhar()
            elif self._estado == "vitória":
                self._tela.blit(self._fonte.render(f"Vitória! Pontuação: {self._pontos_finais}", True, (0, 255, 0)), (Constantes.LARGURA // 2 - 200, Constantes.ALTURA // 2))
                if any(e.type == pygame.KEYDOWN for e in eventos):
                    self._estado = "menu"

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        sys.exit()

    def processar_escolha_menu(self, escolha: Optional[str]) -> bool:
        if escolha == "Jogar":
            self._estado = "menu_jogar"
        elif escolha == "Score": 
            self._estado = "ranking"
            self._ranking_manager.carregar_de_arquivo()
        elif escolha == "Sobre": 
            self._estado = "menu2"
        elif escolha == "Configurações": 
            self._estado = "config"
        elif escolha == "Sair": 
            return False
        return True

    def processar_escolha_submenu(self, escolha: str):
        if escolha == "Continuar":
            if self.carregar_progresso_jogo():
                self._estado = "batalha"
        elif escolha == "Novo Jogo":
            self._estado = "jogar"
            self._nome_jogador.ativar()

    def processar_escolha_game_over(self, escolha: Optional[str]) -> bool:
        if escolha == "Continuar":
            if self.carregar_progresso_jogo():
                self._estado = "batalha"
            else:
                self._estado = "jogar"
                self._nome_jogador.ativar()
        elif escolha == "Novo Jogo":
            self._estado = "jogar"
            self._nome_jogador.ativar()
        elif escolha == "Sair para Menu":
            self._estado = "menu"
        return True

    def _adicionar_ao_ranking(self, pontuacao: int) -> None:
        if self._nome_jogador_atual:
            jogador = JogadorRanking(self._nome_jogador_atual, pontuacao)
            self._ranking_manager.adicionar_jogador(jogador)

    def salvar_progresso_jogo(self) -> None: 
        save_data = {
            "nome_jogador_atual": self._nome_jogador_atual,
            "batalha_estado": self._batalha.to_dict()
        }
        try:
            with open("../assets/ranking/save_game.json", "w") as f:
                json.dump(save_data, f, indent=4)
        except IOError as e:
            print(f"Erro ao salvar o jogo: {e}")
            
    def carregar_progresso_jogo(self) -> bool: 
        try:
            with open("../assets/ranking/save_game.json", "r") as f:
                save_data = json.load(f)
            
            self._nome_jogador_atual = save_data.get("nome_jogador_atual")
            if self._nome_jogador_atual is None:
                return False
                
            batalha_data = save_data.get("batalha_estado")
            if batalha_data:
                self._batalha.from_dict(batalha_data)
                return True
            return False
        except (IOError, json.JSONDecodeError) as e:
            print(f"Não foi possível carregar o jogo salvo: {e}")
            return False
    
    def mostrar_menu_pausa(self) -> None:
        em_pausa = True
        fonte_pausa = pygame.font.SysFont(None, 60)
        opcoes = ["Continuar", "Salvar e Voltar ao Menu"]
        opcao_selecionada = 0

        while em_pausa:
            self._tela.fill((0, 0, 0))

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        em_pausa = False
                    elif evento.key == pygame.K_UP:
                        opcao_selecionada = (opcao_selecionada - 1) % len(opcoes)
                    elif evento.key == pygame.K_DOWN:
                        opcao_selecionada = (opcao_selecionada + 1) % len(opcoes)
                    elif evento.key == pygame.K_RETURN:
                        if opcoes[opcao_selecionada] == "Continuar":
                            em_pausa = False
                        elif opcoes[opcao_selecionada] == "Salvar e Voltar ao Menu":
                            self.salvar_progresso_jogo()
                            self._estado = "menu"
                            em_pausa = False

            for i, texto in enumerate(opcoes):
                cor = (255, 255, 0) if i == opcao_selecionada else (255, 255, 255)
                superficie_texto = fonte_pausa.render(texto, True, cor)
                pos_x = Constantes.LARGURA // 2 - superficie_texto.get_width() // 2
                pos_y = 250 + i * 80
                self._tela.blit(superficie_texto, (pos_x, pos_y))

            pygame.display.update()