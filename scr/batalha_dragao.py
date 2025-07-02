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
        self._game = game
        self._tela = tela
        self._asset_manager = asset_manager

        self._fundo_batalha = self._asset_manager.get_imagem('fundobatalha')
        self._fundo_batalha = pygame.transform.scale(
            self._fundo_batalha, (Constantes.LARGURA, Constantes.ALTURA))

        self._fundo_largura = self._fundo_batalha.get_width()
        self._fundo_x1, self._fundo_x2 = 0, self._fundo_largura
        self._scroll_speed = 1

        y_chao_batalha = Constantes.ALTURA - 180
        self._jogador = Jogador(asset_manager, y_chao=y_chao_batalha, vida=200)
        self._dragao: Optional[Dragao] = None

        self._fireballs = pygame.sprite.Group()
        self._esqueletos = pygame.sprite.Group()
        self._pocoes = pygame.sprite.Group()
        self._particles = pygame.sprite.Group()
        self._todos_sprites = pygame.sprite.Group(self._jogador)

        try:
            self._font = pygame.font.SysFont(None, 50)
            self._font_ui = pygame.font.SysFont(None, 35)
        except Exception as e:
            print(f"Falha ao carregar SysFont na batalha: {e}")
            self._font = self._asset_manager.fonte_50
            self._font_ui = self._asset_manager.fonte_30

        self._timer_esqueleto = pygame.time.get_ticks()

        self._fase_batalha = 1
        self._inimigos_para_fase_2 = 5
        self._derrotados = 0
        self._pontuacao_final = 0

    def get_pontuacao_final(self) -> int:
        return self._pontuacao_final
        
    def get_jogador(self) -> Jogador:
        return self._jogador

    def _update_fundo_loop(self) -> None:
        self._fundo_x1 -= self._scroll_speed
        self._fundo_x2 -= self._scroll_speed
        if self._fundo_x1 <= -self._fundo_largura:
            self._fundo_x1 = self._fundo_x2 + self._fundo_largura
        if self._fundo_x2 <= -self._fundo_largura:
            self._fundo_x2 = self._fundo_x1 + self._fundo_largura

    def _gerenciar_fases(self):
        if self._fase_batalha == 1:
            agora = pygame.time.get_ticks()
            if agora - self._timer_esqueleto > 3000 and len(self._esqueletos) < 3:
                self._timer_esqueleto = agora
                spawn_x = Constantes.LARGURA + random.randint(50, 150)
                esqueleto = Esqueleto(
                    spawn_x, self._jogador.y_chao, self._asset_manager, vida=100)
                self._esqueletos.add(esqueleto)
                self._todos_sprites.add(esqueleto)

            if self._derrotados >= self._inimigos_para_fase_2:
                self._fase_batalha = 2
                self._game.salvar_progresso_jogo()

        if self._fase_batalha == 2 and self._dragao is None:
            self._dragao = Dragao(
                x=0, y=0, asset_manager=self._asset_manager, grupo_projeteis=self._fireballs)
            self._dragao.get_rect().right = Constantes.LARGURA - 100
            self._dragao.get_rect().bottom = self._jogador.y_chao
            self._todos_sprites.add(self._dragao)

    def _criar_particulas_sangue(self, pos: tuple[int, int]) -> None:
        for _ in range(10):
            self._particles.add(Particle(pos, (255, 0, 0)))

    def _checar_colisoes(self) -> None:
        if self._jogador.pode_causar_dano():
            atingidos = pygame.sprite.spritecollide(
                self._jogador, self._esqueletos, False)
            for esqueleto in atingidos:
                if abs(self._jogador.get_rect().centerx - esqueleto.get_rect().centerx) < 120:
                    esqueleto.receber_dano(25)
                    self._pontuacao_final += 25
                    self._criar_particulas_sangue(esqueleto.get_rect().center)
                    if not esqueleto.vivo:
                        self._derrotados += 1
                        self._pontuacao_final += 100
                        if random.random() < 0.5:
                            pocao = Pocao(
                                esqueleto.get_rect().center, self._asset_manager)
                            self._pocoes.add(pocao)
                            self._todos_sprites.add(pocao)
                        esqueleto.kill()

            if self._dragao and self._dragao.vivo and pygame.sprite.collide_rect(self._jogador, self._dragao):
                if abs(self._jogador.get_rect().centerx - self._dragao.get_rect().centerx) < 350:
                    self._dragao.receber_dano(25)
                    self._pontuacao_final += 25
                    self._criar_particulas_sangue(self._dragao.get_rect().center)

        for esqueleto in self._esqueletos:
            if esqueleto.pode_causar_dano() and pygame.sprite.collide_rect(esqueleto, self._jogador):
                if not self._jogador.defendendo:
                    self._jogador.receber_dano(esqueleto.get_dano())
                    self._criar_particulas_sangue(self._jogador.get_rect().center)

        if self._dragao:
            atingido_por_fireball = pygame.sprite.spritecollide(
                self._jogador, self._fireballs, True)
            if atingido_por_fireball and not self._jogador.defendendo:
                self._jogador.receber_dano(20)

        coletadas = pygame.sprite.spritecollide(
            self._jogador, self._pocoes, True)
        if coletadas:
            self._jogador.coletar_pocao()

    def atualizar(self, volume_efeitos: float) -> Optional[str]:
        teclas = pygame.key.get_pressed()
        self._update_fundo_loop()

        self._jogador.update(teclas, volume_efeitos)
        self._esqueletos.update(self._jogador.get_rect())
        if self._dragao:
            self._dragao.update(self._jogador.get_rect())

        self._fireballs.update()
        self._particles.update()
        self._pocoes.update()

        self._gerenciar_fases()
        self._checar_colisoes()

        if not self._jogador.vivo and self._jogador.get_acao() == 'morrer' and self._jogador.get_indice_frame() >= len(self._jogador.get_animacoes()['morrer']) - 1:
            return "Derrota"
        if self._dragao and not self._dragao.vivo and self._dragao.get_acao() == 'morrer' and self._dragao.get_indice_frame() >= len(self._dragao.get_animacoes()['morrer']) - 1:
            self._pontuacao_final += 1000
            return "Vitória"

        return None

    def desenhar_barra_vida(self, surf, x, y, pct, cor_cheia, cor_vazia, largura_barra=250, altura_barra=25):
        if pct < 0: pct = 0
        if pct > 100: pct = 100

        preenchimento = (pct / 100) * largura_barra
        borda_rect = pygame.Rect(x, y, largura_barra, altura_barra)
        preenchimento_rect = pygame.Rect(x, y, preenchimento, altura_barra)

        pygame.draw.rect(surf, cor_vazia, borda_rect)
        pygame.draw.rect(surf, cor_cheia, preenchimento_rect)
        pygame.draw.rect(surf, Constantes.BRANCO, borda_rect, 3)

    def desenhar(self) -> None:
        self._tela.blit(self._fundo_batalha, (self._fundo_x1, 0))
        self._tela.blit(self._fundo_batalha, (self._fundo_x2, 0))

        self._todos_sprites.draw(self._tela)
        self._fireballs.draw(self._tela)
        for p in self._particles:
            p.draw(self._tela)

        MARGEM_LATERAL, MARGEM_SUPERIOR = 200, 120
        LARGURA_BARRA_VIDA, ALTURA_BARRA_VIDA = 280, 30
        ESPACO_TEXTO_Y = 35

        y_atual = 120
        pct_jogador = (self._jogador.vida / self._jogador.get_vida_maxima()) * 100 if self._jogador.get_vida_maxima() > 0 else 0
        self.desenhar_barra_vida(self._tela, MARGEM_LATERAL, y_atual, pct_jogador, Constantes.VERDE, Constantes.VERMELHO, LARGURA_BARRA_VIDA, ALTURA_BARRA_VIDA)
        y_atual += ALTURA_BARRA_VIDA + 5

        vida_jogador_txt = f"Vida: {self._jogador.vida} / {self._jogador.get_vida_maxima()}"
        vida_jogador_surf = self._font_ui.render(vida_jogador_txt, True, Constantes.BRANCO)
        self._tela.blit(vida_jogador_surf, (MARGEM_LATERAL, y_atual))
        y_atual += ESPACO_TEXTO_Y

        pocao_txt = self._font_ui.render(f"Poções (H): {self._jogador.num_pocoes}", True, Constantes.BRANCO)
        self._tela.blit(pocao_txt, (MARGEM_LATERAL, y_atual))
        y_atual += ESPACO_TEXTO_Y

        agora = pygame.time.get_ticks()
        cooldown_restante = max(0, (self._jogador.get_last_dash_time() + self._jogador.get_dash_cooldown()) - agora)
        pronto_para_dash = cooldown_restante == 0
        dash_cor = Constantes.VERDE if pronto_para_dash else Constantes.AMARELO
        dash_txt_str = f"Investida (Shift): {'Pronta!' if pronto_para_dash else f'{(cooldown_restante / 1000):.1f}s'}"
        dash_txt = self._font_ui.render(dash_txt_str, True, dash_cor)
        self._tela.blit(dash_txt, (MARGEM_LATERAL, y_atual))

        if self._dragao:
            MARGEM_LATERAL_DRAGAO = 200
            x_barra_dragao = Constantes.LARGURA - LARGURA_BARRA_VIDA - MARGEM_LATERAL_DRAGAO
            y_atual_dragao = MARGEM_SUPERIOR
            pct_dragao = (self._dragao.vida / self._dragao.get_vida_maxima()) * 100 if self._dragao.get_vida_maxima() > 0 else 0
            self.desenhar_barra_vida(self._tela, x_barra_dragao, y_atual_dragao, pct_dragao, (150, 0, 150), Constantes.VERMELHO, LARGURA_BARRA_VIDA, ALTURA_BARRA_VIDA)
            y_atual_dragao += ALTURA_BARRA_VIDA + 5

            vida_dragao_txt = f"Vida: {self._dragao.vida} / {self._dragao.get_vida_maxima()}"
            vida_dragao_surf = self._font_ui.render(vida_dragao_txt, True, Constantes.BRANCO)
            vida_dragao_rect = vida_dragao_surf.get_rect(y=y_atual_dragao, right=x_barra_dragao + LARGURA_BARRA_VIDA - 5)
            self._tela.blit(vida_dragao_surf, vida_dragao_rect)

        pontos_txt = self._font.render(f"Pontuação: {self._pontuacao_final}", True, Constantes.BRANCO)
        pontos_rect = pontos_txt.get_rect(centerx=Constantes.LARGURA / 2, y=MARGEM_SUPERIOR)
        self._tela.blit(pontos_txt, pontos_rect)

        for sprite in self._todos_sprites:
            if hasattr(sprite, 'get_grupo_popup_dano'):
                sprite.get_grupo_popup_dano().draw(self._tela)

    def reset_batalha(self) -> None:
        self._jogador.reset()
        self._dragao = None
        self._esqueletos.empty()
        self._pocoes.empty()
        self._particles.empty()
        self._fireballs.empty()
        self._todos_sprites.empty()
        self._todos_sprites.add(self._jogador)
        self._fase_batalha = 1
        self._derrotados = 0
        self._pontuacao_final = 0
        self._timer_esqueleto = pygame.time.get_ticks()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "jogador": self._jogador.to_dict(),
            "dragao": self._dragao.to_dict() if self._dragao else None,
            "esqueletos": [e.to_dict() for e in self._esqueletos],
            "fase_batalha": self._fase_batalha,
            "derrotados": self._derrotados,
            "pontuacao_final": self._pontuacao_final
        }

    def from_dict(self, data: Dict[str, Any]) -> None:
        self.reset_batalha()

        jogador_data = data.get("jogador")
        if jogador_data:
            self._jogador = Jogador.from_dict(jogador_data, self._asset_manager)
            self._todos_sprites.add(self._jogador)

        esqueletos_data = data.get("esqueletos", [])
        y_chao_batalha = self._jogador.y_chao
        for esqueleto_data in esqueletos_data:
            esqueleto = Esqueleto(
                x=esqueleto_data.get("x", Constantes.LARGURA),
                y_chao=y_chao_batalha,
                asset_manager=self._asset_manager
            )
            esqueleto.vida = esqueleto_data.get("vida", 100)
            esqueleto.get_rect().x = esqueleto_data.get("x", Constantes.LARGURA)
            esqueleto.get_rect().bottom = y_chao_batalha
            esqueleto.set_direcao(esqueleto_data.get("direcao", -1))
            self._esqueletos.add(esqueleto)
            self._todos_sprites.add(esqueleto)

        self._fase_batalha = data.get("fase_batalha", 1)
        self._derrotados = data.get("derrotados", 0)
        self._pontuacao_final = data.get("pontuacao_final", 0)

        dragao_data = data.get("dragao")
        if dragao_data:
            y_dragao = self._jogador.y_chao
            self._dragao = Dragao.from_dict(dragao_data, self._asset_manager, self._fireballs)
            self._dragao.get_rect().bottom = y_dragao
            self._todos_sprites.add(self._dragao)