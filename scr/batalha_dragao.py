import pygame
import random
from typing import Optional, TYPE_CHECKING, Dict, Any

from constantes import Constantes
from asset_manager import AssetManager
from jogador import Jogador
from esqueleto import Esqueleto
from dragao import Dragao
from pocao import Pocao
from particle import Particle

if TYPE_CHECKING:
    from game import Game


class BatalhaDragao:
    def __init__(self, game: 'Game', tela: pygame.Surface, asset_manager: AssetManager) -> None:
        self.game = game
        self.tela = tela
        self.asset_manager = asset_manager

        self.fundo_batalha = self.asset_manager.get_imagem('fundobatalha')
        self.fundo_batalha = pygame.transform.scale(
            self.fundo_batalha, (Constantes.LARGURA, Constantes.ALTURA))

        self.fundo_largura = self.fundo_batalha.get_width()
        self.fundo_x1, self.fundo_x2 = 0, self.fundo_largura
        self.scroll_speed = 1

        y_chao_batalha = Constantes.ALTURA - 180
        self.jogador = Jogador(asset_manager, y_chao=y_chao_batalha, vida=200)
        self.dragao: Optional[Dragao] = None

        self.fireballs = pygame.sprite.Group()
        self.esqueletos = pygame.sprite.Group()
        self.pocoes = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()
        self.todos_sprites = pygame.sprite.Group(self.jogador)

        try:
            self.font = pygame.font.SysFont(None, 50)
            self.font_ui = pygame.font.SysFont(None, 35)
        except Exception as e:
            print(f"Falha ao carregar SysFont na batalha: {e}")
            self.font = self.asset_manager.fonte_50
            self.font_ui = self.asset_manager.fonte_30

        self.timer_esqueleto = pygame.time.get_ticks()

        self._fase_batalha = 1
        self._inimigos_para_fase_2 = 5
        self._derrotados = 0
        self.pontuacao_final = 0

    def get_pontuacao_final(self) -> int:
        return self.pontuacao_final

    def _update_fundo_loop(self) -> None:
        self.fundo_x1 -= self.scroll_speed
        self.fundo_x2 -= self.scroll_speed
        if self.fundo_x1 <= -self.fundo_largura:
            self.fundo_x1 = self.fundo_x2 + self.fundo_largura
        if self.fundo_x2 <= -self.fundo_largura:
            self.fundo_x2 = self.fundo_x1 + self.fundo_largura

    def _gerenciar_fases(self):
        if self._fase_batalha == 1:
            agora = pygame.time.get_ticks()
            if agora - self.timer_esqueleto > 3000 and len(self.esqueletos) < 3:
                self.timer_esqueleto = agora
                spawn_x = Constantes.LARGURA + random.randint(50, 150)
                esqueleto = Esqueleto(
                    spawn_x, self.jogador.y_chao, self.asset_manager, vida=100)
                self.esqueletos.add(esqueleto)
                self.todos_sprites.add(esqueleto)

            if self._derrotados >= self._inimigos_para_fase_2:
                self._fase_batalha = 2
                self.game.salvar_progresso_jogo()

        if self._fase_batalha == 2 and self.dragao is None:
            self.dragao = Dragao(
                x=0, y=0, asset_manager=self.asset_manager, grupo_projeteis=self.fireballs)
            self.dragao.rect.right = Constantes.LARGURA - 100
            self.dragao.rect.bottom = self.jogador.y_chao
            self.todos_sprites.add(self.dragao)

    def _criar_particulas_sangue(self, pos: tuple[int, int]) -> None:
        for _ in range(10):
            self.particles.add(Particle(pos, (255, 0, 0)))

    def _checar_colisoes(self) -> None:
        if self.jogador.pode_causar_dano():
            atingidos = pygame.sprite.spritecollide(
                self.jogador, self.esqueletos, False)
            for esqueleto in atingidos:
                if abs(self.jogador.rect.centerx - esqueleto.rect.centerx) < 120:
                    esqueleto.receber_dano(25)
                    self.pontuacao_final += 25
                    self._criar_particulas_sangue(esqueleto.rect.center)
                    if not esqueleto.vivo:
                        self._derrotados += 1
                        self.pontuacao_final += 100
                        if random.random() < 0.5:
                            pocao = Pocao(
                                esqueleto.rect.center, self.asset_manager)
                            self.pocoes.add(pocao)
                            self.todos_sprites.add(pocao)
                        esqueleto.kill()

            if self.dragao and self.dragao.vivo and pygame.sprite.collide_rect(self.jogador, self.dragao):
                if abs(self.jogador.rect.centerx - self.dragao.rect.centerx) < 350:
                    self.dragao.receber_dano(25)
                    self.pontuacao_final += 25
                    self._criar_particulas_sangue(self.dragao.rect.center)

        for esqueleto in self.esqueletos:
            if esqueleto.pode_causar_dano() and pygame.sprite.collide_rect(esqueleto, self.jogador):
                if not self.jogador.defendendo:
                    self.jogador.receber_dano(esqueleto.dano)
                    self._criar_particulas_sangue(self.jogador.rect.center)

        if self.dragao:
            atingido_por_fireball = pygame.sprite.spritecollide(
                self.jogador, self.fireballs, True)
            if atingido_por_fireball and not self.jogador.defendendo:
                self.jogador.receber_dano(20)

        coletadas = pygame.sprite.spritecollide(
            self.jogador, self.pocoes, True)
        if coletadas:
            self.jogador.coletar_pocao()

    def atualizar(self, volume_efeitos: float) -> Optional[str]:
        teclas = pygame.key.get_pressed()
        self._update_fundo_loop()

        self.jogador.update(teclas, volume_efeitos)
        self.esqueletos.update(self.jogador.rect)
        if self.dragao:
            self.dragao.update(self.jogador.rect)

        self.fireballs.update()
        self.particles.update()
        self.pocoes.update()

        self._gerenciar_fases()
        self._checar_colisoes()

        if not self.jogador.vivo and self.jogador.acao == 'morrer' and self.jogador.indice_frame >= len(self.jogador.animacoes['morrer']) - 1:
            return "Derrota"
        if self.dragao and not self.dragao.vivo and self.dragao.acao == 'morrer' and self.dragao.indice_frame >= len(self.dragao.animacoes['morrer']) - 1:
            self.pontuacao_final += 1000
            return "Vitória"

        return None

    def desenhar_barra_vida(self, surf, x, y, pct, cor_cheia, cor_vazia, largura_barra=250, altura_barra=25):
        if pct < 0:
            pct = 0
        if pct > 100:
            pct = 100

        preenchimento = (pct / 100) * largura_barra
        borda_rect = pygame.Rect(x, y, largura_barra, altura_barra)
        preenchimento_rect = pygame.Rect(x, y, preenchimento, altura_barra)

        pygame.draw.rect(surf, cor_vazia, borda_rect)
        pygame.draw.rect(surf, cor_cheia, preenchimento_rect)
        pygame.draw.rect(surf, Constantes.BRANCO, borda_rect, 3)

    def desenhar(self) -> None:
        self.tela.blit(self.fundo_batalha, (self.fundo_x1, 0))
        self.tela.blit(self.fundo_batalha, (self.fundo_x2, 0))

        self.todos_sprites.draw(self.tela)
        self.fireballs.draw(self.tela)
        for p in self.particles:
            p.draw(self.tela)

        MARGEM_LATERAL = 200
        MARGEM_SUPERIOR = 120
        LARGURA_BARRA_VIDA = 280
        ALTURA_BARRA_VIDA = 30
        ESPACO_TEXTO_Y = 35

        y_atual = 120
        pct_jogador = (self.jogador.vida / self.jogador.vida_maxima) * \
            100 if self.jogador.vida_maxima > 0 else 0
        self.desenhar_barra_vida(self.tela, MARGEM_LATERAL, y_atual,
                                 pct_jogador, Constantes.VERDE, Constantes.VERMELHO, LARGURA_BARRA_VIDA, ALTURA_BARRA_VIDA)
        y_atual += ALTURA_BARRA_VIDA + 5

        vida_jogador_txt = f"Vida: {self.jogador.vida} / {self.jogador.vida_maxima}"
        vida_jogador_surf = self.font_ui.render(
            vida_jogador_txt, True, Constantes.BRANCO)
        self.tela.blit(vida_jogador_surf, (MARGEM_LATERAL, y_atual))
        y_atual += ESPACO_TEXTO_Y

        pocao_txt = self.font_ui.render(
            f"Poções (H): {self.jogador.num_pocoes}", True, Constantes.BRANCO)
        self.tela.blit(pocao_txt, (MARGEM_LATERAL, y_atual))
        y_atual += ESPACO_TEXTO_Y

        agora = pygame.time.get_ticks()
        cooldown_restante = max(
            0, (self.jogador.last_dash_time + self.jogador.dash_cooldown) - agora)
        pronto_para_dash = cooldown_restante == 0
        dash_cor = Constantes.VERDE if pronto_para_dash else Constantes.AMARELO
        dash_txt_str = f"Investida (Shift): {'Pronta!' if pronto_para_dash else f'{(cooldown_restante / 1000):.1f}s'}"
        dash_txt = self.font_ui.render(dash_txt_str, True, dash_cor)
        self.tela.blit(dash_txt, (MARGEM_LATERAL, y_atual))

        if self.dragao:
            MARGEM_LATERAL_DRAGAO = 200
            x_barra_dragao = Constantes.LARGURA - LARGURA_BARRA_VIDA - MARGEM_LATERAL_DRAGAO
            y_atual_dragao = MARGEM_SUPERIOR
            pct_dragao = (self.dragao.vida / self.dragao.vida_maxima) * \
                100 if self.dragao.vida_maxima > 0 else 0
            self.desenhar_barra_vida(self.tela, x_barra_dragao, y_atual_dragao, pct_dragao, (
                150, 0, 150), Constantes.VERMELHO, LARGURA_BARRA_VIDA, ALTURA_BARRA_VIDA)
            y_atual_dragao += ALTURA_BARRA_VIDA + 5

            vida_dragao_txt = f"Vida: {self.dragao.vida} / {self.dragao.vida_maxima}"
            vida_dragao_surf = self.font_ui.render(
                vida_dragao_txt, True, Constantes.BRANCO)
            vida_dragao_rect = vida_dragao_surf.get_rect()
            vida_dragao_rect.y = y_atual_dragao
            vida_dragao_rect.right = x_barra_dragao + LARGURA_BARRA_VIDA - 5
            self.tela.blit(vida_dragao_surf, vida_dragao_rect)

        pontos_txt = self.font.render(
            f"Pontuação: {self.pontuacao_final}", True, Constantes.BRANCO)
        pontos_rect = pontos_txt.get_rect(
            centerx=Constantes.LARGURA / 2, y=MARGEM_SUPERIOR)
        self.tela.blit(pontos_txt, pontos_rect)

        for sprite in self.todos_sprites:
            if hasattr(sprite, 'grupo_popup_dano'):
                sprite.grupo_popup_dano.draw(self.tela)

    def reset_batalha(self) -> None:
        self.jogador.reset()
        self.dragao = None
        self.esqueletos.empty()
        self.pocoes.empty()
        self.particles.empty()
        self.fireballs.empty()
        self.todos_sprites.empty()
        self.todos_sprites.add(self.jogador)
        self._fase_batalha = 1
        self._derrotados = 0
        self.pontuacao_final = 0
        self.timer_esqueleto = pygame.time.get_ticks()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "jogador": self.jogador.to_dict(),
            "dragao": self.dragao.to_dict() if self.dragao else None,
            "esqueletos": [e.to_dict() for e in self.esqueletos],
            "fase_batalha": self._fase_batalha,
            "derrotados": self._derrotados,
            "pontuacao_final": self.pontuacao_final
        }

    def from_dict(self, data: Dict[str, Any]) -> None:
        self.reset_batalha()

        jogador_data = data.get("jogador")
        if jogador_data:
            self.jogador = Jogador.from_dict(jogador_data, self.asset_manager)
            self.todos_sprites.add(self.jogador)

        esqueletos_data = data.get("esqueletos", [])
        y_chao_batalha = self.jogador.y_chao
        for esqueleto_data in esqueletos_data:
            esqueleto = Esqueleto(
                x=esqueleto_data.get("x", Constantes.LARGURA),
                y_chao=y_chao_batalha,
                asset_manager=self.asset_manager
            )
            esqueleto.vida = esqueleto_data.get("vida", 100)
            esqueleto.rect.x = esqueleto_data.get("x", Constantes.LARGURA)
            esqueleto.rect.bottom = y_chao_batalha
            esqueleto.direcao = esqueleto_data.get("direcao", -1)
            self.esqueletos.add(esqueleto)
            self.todos_sprites.add(esqueleto)

        self._fase_batalha = data.get("fase_batalha", 1)
        self._derrotados = data.get("derrotados", 0)
        self.pontuacao_final = data.get("pontuacao_final", 0)

        dragao_data = data.get("dragao")
        if dragao_data:
            y_dragao = self.jogador.y_chao
            self.dragao = Dragao.from_dict(
                dragao_data, self.asset_manager, self.fireballs)
            self.dragao.rect.bottom = y_dragao
            self.todos_sprites.add(self.dragao)