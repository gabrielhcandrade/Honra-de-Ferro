import pygame
import sys
from pygame import mixer
import json
from typing import Optional, List

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

        self.fullscreen: bool = False
        self.tela: pygame.Surface = pygame.display.set_mode((Constantes.LARGURA, Constantes.ALTURA))
        pygame.display.set_caption("Honra de Ferro")

        self.asset_manager = AssetManager()

        self.fundo = self.asset_manager.get_imagem('fundo')
        self.fundo = pygame.transform.scale(self.fundo, (Constantes.LARGURA, Constantes.ALTURA))

        self.fundo2 = self.asset_manager.get_imagem('fundo2')
        self.fundo2 = pygame.transform.scale(self.fundo2, (Constantes.LARGURA, Constantes.ALTURA))

        try:
            mixer.music.load("../assets/sons/abertura.mp3")
            mixer.music.set_volume(0.1)
            mixer.music.play(-1)
        except pygame.error as e:
            print(f"Erro ao carregar ou tocar abertura.mp3: {e}")

        self.fonte = self.asset_manager.fonte_50
        self.fonte_titulo = self.asset_manager.fonte_100

        self.titulo_texto = self.fonte_titulo.render("Honra de Ferro", True, Constantes.PRETO)
        self.titulo_rect = self.titulo_texto.get_rect(center=(Constantes.LARGURA // 2, 220))

        botoes: List[Button] = [
            Button("Jogar", (Constantes.LARGURA // 2, 360), self.fonte),
            Button("Score", (Constantes.LARGURA // 2, 470), self.fonte),
            Button("Configurações", (Constantes.LARGURA // 2, 580), self.fonte),
            Button("Sobre", (Constantes.LARGURA // 2, 690), self.fonte),
            Button("Sair", (Constantes.LARGURA // 2, 800), self.fonte),
        ]

        self.estado: str = "menu"
        self.nome_jogador_atual: Optional[str] = None
        self.pontos_finais: int = 0

        self.ranking_manager: RankingManager = RankingManager()
        self.menu: Menu = Menu(self.tela, self.fundo, botoes, self.fonte)
        self.config: ConfigScreen = ConfigScreen(self)
        self.menu2: Menu2 = Menu2(self.tela, self.asset_manager)
        self.nome_jogador: NomeJogador = NomeJogador(self.ranking_manager)
        self.batalha: BatalhaDragao = BatalhaDragao(self, self.tela, self.asset_manager)
        self.game_over_screen: GameOverScreen = GameOverScreen(self.tela)
        self.tela_ranking_pygame: TelaRankingPygame = TelaRankingPygame(self.tela, self.ranking_manager)

    def executar(self) -> None:
        clock: pygame.time.Clock = pygame.time.Clock()
        rodando: bool = True

        while rodando:
            eventos: List[pygame.event.Event] = pygame.event.get()

            if self.estado == "config":
                self.config.processar_eventos(eventos)

            for evento in eventos:
                if evento.type == pygame.QUIT:
                    rodando = False

                if evento.type == pygame.KEYDOWN:
                    if self.estado == "menu":
                        if evento.key == pygame.K_UP: self.menu.mover_selecao(-1)
                        elif evento.key == pygame.K_DOWN: self.menu.mover_selecao(1)
                        elif evento.key == pygame.K_RETURN: rodando = self.processar_escolha_menu(self.menu.opcao_selecionada())
                    elif self.estado == "jogar":
                        resultado = self.nome_jogador.processar_evento(evento)
                        if resultado == "confirmado":
                            self.nome_jogador_atual = self.nome_jogador.get_nome()
                            self.estado = "batalha"
                            self.batalha.reset_batalha()
                            self.salvar_progresso_jogo()
                        elif resultado == "voltar": self.estado = "menu"
                    elif self.estado in ["ranking", "config", "menu2"]:
                        if evento.key == pygame.K_ESCAPE: self.estado = "menu"
                    elif self.estado == "game_over":
                        if evento.key == pygame.K_UP: self.game_over_screen.mover_selecao(-1)
                        elif evento.key == pygame.K_DOWN: self.game_over_screen.mover_selecao(1)
                        elif evento.key == pygame.K_RETURN: rodando = self.processar_escolha_game_over(self.game_over_screen.opcao_escolhida())

                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if self.estado == "menu":
                        escolha_mouse = self.menu.verificar_clique(evento.pos)
                        if escolha_mouse: rodando = self.processar_escolha_menu(escolha_mouse)
                    elif self.estado == "game_over":
                        escolha_mouse = self.game_over_screen.verificar_clique(evento.pos)
                        if escolha_mouse: rodando = self.processar_escolha_game_over(escolha_mouse)

            self.tela.fill(Constantes.PRETO)
            if self.estado == "menu":
                self.menu.desenhar()
                self.tela.blit(self.titulo_texto, self.titulo_rect)
            elif self.estado == "config":
                self.config.desenhar(self.tela)
            elif self.estado == "menu2":
                self.menu2.desenhar()
            elif self.estado == "jogar":
                self.nome_jogador.desenhar(self.tela)
            elif self.estado == "batalha":
                for evento in eventos:
                    if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                        self.mostrar_menu_pausa()
                # CORREÇÃO: Passa o volume dos efeitos para a atualização da batalha.
                resultado = self.batalha.atualizar(self.config.volume_efeitos)
                self.batalha.desenhar()
                if resultado:
                    self.pontos_finais = self.batalha.get_pontuacao_final()
                    if resultado == "Vitória":
                        self._adicionar_ao_ranking(self.pontos_finais)
                        self.estado = "vitória"
                    else:
                        self.estado = "game_over"
            elif self.estado == "game_over":
                self.game_over_screen.desenhar()
            elif self.estado == "ranking":
                self.tela_ranking_pygame.desenhar()
            elif self.estado == "vitória":
                self.tela.blit(self.fonte.render(f"Vitória! Pontuação: {self.pontos_finais}", True, (0, 255, 0)), (Constantes.LARGURA // 2 - 200, Constantes.ALTURA // 2))
                if any(event.type == pygame.KEYDOWN for event in eventos):
                    self.estado = "menu"

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        sys.exit()

    def processar_escolha_menu(self, escolha: Optional[str]) -> bool:
        if escolha == "Jogar": self.estado = "jogar"; self.nome_jogador.ativar()
        elif escolha == "Score": self.estado = "ranking"; self.ranking_manager.carregar_de_arquivo()
        elif escolha == "Sobre": self.estado = "menu2"
        elif escolha == "Configurações": self.estado = "config"
        elif escolha == "Sair": return False
        return True

    def processar_escolha_game_over(self, escolha: Optional[str]) -> bool:
        if escolha == "Continuar":
            if self.carregar_progresso_jogo():
                self.estado = "batalha"
            else:
                self.estado = "jogar"
                self.nome_jogador.ativar()
        elif escolha == "Novo Jogo":
            self.estado = "jogar"
            self.nome_jogador.ativar()
        elif escolha == "Sair para Menu":
            self.estado = "menu"
        return True

    def _adicionar_ao_ranking(self, pontuacao: int) -> None:
        if self.nome_jogador_atual:
            jogador = JogadorRanking(self.nome_jogador_atual, pontuacao)
            self.ranking_manager.adicionar_jogador(jogador)

    def salvar_progresso_jogo(self) -> None: 
        save_data = {
            "nome_jogador_atual": self.nome_jogador_atual,
            "batalha_estado": self.batalha.to_dict()
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
            
            self.nome_jogador_atual = save_data.get("nome_jogador_atual")
            if self.nome_jogador_atual is None:
                return False
                
            batalha_data = save_data.get("batalha_estado")
            if batalha_data:
                self.batalha.from_dict(batalha_data)
                return True
            return False
        except (IOError, json.JSONDecodeError) as e:
            print(f"Não foi possível carregar o jogo salvo: {e}")
            return False
    
    def mostrar_menu_pausa(self) -> None:
        em_pausa = True
        fonte_pausa = pygame.font.SysFont(None, 60)
        opcoes = ["Continuar", "Voltar ao Menu"]
        opcao_selecionada = 0

        while em_pausa:
            self.tela.fill((0, 0, 0))

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
                        elif opcoes[opcao_selecionada] == "Voltar ao Menu":
                            self.estado = "menu"
                            em_pausa = False

            for i, texto in enumerate(opcoes):
                cor = (255, 255, 0) if i == opcao_selecionada else (255, 255, 255)
                superficie_texto = fonte_pausa.render(texto, True, cor)
                pos_x = Constantes.LARGURA // 2 - superficie_texto.get_width() // 2
                pos_y = 250 + i * 80
                self.tela.blit(superficie_texto, (pos_x, pos_y))

            pygame.display.update()