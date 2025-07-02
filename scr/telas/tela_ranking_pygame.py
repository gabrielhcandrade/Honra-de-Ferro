import pygame
from typing import Tuple
from componentes.ranking_manager import RankingManager 
from constantes import Constantes

class TelaRankingPygame:
    def __init__(self, tela: pygame.Surface, ranking_manager: RankingManager) -> None:
        self._tela = tela
        self._ranking_manager = ranking_manager
        self._fonte_titulo: pygame.font.Font = pygame.font.Font(None, 80) 
        
        try:
            self._fonte_itens: pygame.font.Font = pygame.font.SysFont('monospace', 40)
        except pygame.error:
            self._fonte_itens: pygame.font.Font = pygame.font.Font(None, 45)
        self._fonte_instrucao: pygame.font.Font = pygame.font.Font(None, 36)

        self._cor_fundo: Tuple[int, int, int] = (20, 20, 60)
        self._cor_titulo: Tuple[int, int, int] = Constantes.COR_SELECIONADA
        self._cor_texto_ranking: Tuple[int, int, int] = Constantes.COR_TEXTO

    def desenhar(self) -> None:
        self._tela.fill(self._cor_fundo)

        titulo_surf: pygame.Surface = self._fonte_titulo.render("Ranking - Top 10", True, self._cor_titulo)
        titulo_rect: pygame.Rect = titulo_surf.get_rect(center=(Constantes.LARGURA // 2, Constantes.ALTURA * 0.15))
        self._tela.blit(titulo_surf, titulo_rect)

        y_pos: int = Constantes.ALTURA * 0.3 
        espacamento = 50 

        jogadores = self._ranking_manager.get_jogadores()

        if not jogadores:
            texto_vazio_surf: pygame.Surface = self._fonte_itens.render("Ranking vazio!", True, self._cor_texto_ranking)
            texto_vazio_rect: pygame.Rect = texto_vazio_surf.get_rect(center=(Constantes.LARGURA // 2, y_pos))
            self._tela.blit(texto_vazio_surf, texto_vazio_rect)
        else:
            for i, jogador in enumerate(jogadores[:10]):
                posicao_texto: str = f"{i + 1}."
                nome_texto: str = jogador.get_nome()
                pontos_texto: str = f"{jogador.get_pontuacao()} pts"

                texto_completo: str = f"{posicao_texto:<4} {nome_texto:<20} {pontos_texto:>12}"
                item_surf: pygame.Surface = self._fonte_itens.render(texto_completo, True, self._cor_texto_ranking)
                
                container_rect = pygame.Rect(0, 0, 800, espacamento)
                item_rect: pygame.Rect = item_surf.get_rect(center=container_rect.center)
                
                container_rect.center = (Constantes.LARGURA // 2, y_pos + i * espacamento)
                
                self._tela.blit(item_surf, (container_rect.left + item_rect.left, container_rect.top))

        instrucao_surf: pygame.Surface = self._fonte_instrucao.render("Pressione ESC para voltar", True, Constantes.BRANCO)
        instrucao_rect: pygame.Rect = instrucao_surf.get_rect(center=(Constantes.LARGURA // 2, Constantes.ALTURA - 50))
        self._tela.blit(instrucao_surf, instrucao_rect)