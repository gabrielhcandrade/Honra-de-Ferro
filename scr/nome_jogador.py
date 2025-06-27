import pygame
from typing import Optional, Tuple
from constantes import Constantes
from componentes.ranking_manager import RankingManager

class NomeJogador:
    def __init__(self, ranking_manager: RankingManager) -> None:
        self.ranking_manager = ranking_manager
        self.nome: str = ""
        self.ativo: bool = False
        self.nome_invalido: bool = False
        self.fonte: pygame.font.Font = pygame.font.Font(None, 50)
        self.fonte_pequena: pygame.font.Font = pygame.font.Font(None, 30)
        
        self.input_rect: pygame.Rect = pygame.Rect(0, 0, 500, 60) 
        self.input_rect.center = (Constantes.LARGURA // 2, Constantes.ALTURA // 2)
        self.cursor_visivel: bool = True
        self.cursor_timer: int = pygame.time.get_ticks()

    def ativar(self) -> None:
        self.nome = ""
        self.ativo = True
        self.nome_invalido = False
        self.ranking_manager.carregar_de_arquivo()

    def get_nome(self) -> str:
        return self.nome.strip()

    def processar_evento(self, evento: pygame.event.Event) -> Optional[str]:
        if not self.ativo or evento.type != pygame.KEYDOWN:
            return None

        self.nome_invalido = False

        if evento.key == pygame.K_RETURN:
            nome_final: str = self.get_nome()
            if nome_final:
                if self.ranking_manager.existe_nome(nome_final):
                    self.nome_invalido = True
                    return None
                else:
                    self.ativo = False
                    return "confirmado"
            else:
                return None

        elif evento.key == pygame.K_BACKSPACE:
            self.nome = self.nome[:-1]
        elif evento.key == pygame.K_ESCAPE:
            self.ativo = False
            return "voltar"
        else:
            if len(self.nome) < 15 and (evento.unicode.isalnum() or evento.unicode in [' ', '_', '-']):
                self.nome += evento.unicode

        return None

    def desenhar(self, tela: pygame.Surface) -> None:
        """Desenha a tela de input centralizada."""
        if not self.ativo:
            return

        tela.fill((30, 30, 30))
        prompt: pygame.Surface = self.fonte.render("Digite seu nome:", True, Constantes.COR_TEXTO)
        prompt_rect = prompt.get_rect(center=(Constantes.LARGURA // 2, self.input_rect.top - 60))
        tela.blit(prompt, prompt_rect)

        cor_borda: Tuple[int, int, int] = Constantes.VERMELHO if self.nome_invalido else Constantes.COR_SLIDER
        pygame.draw.rect(tela, (50, 50, 50), self.input_rect, border_radius=10)
        pygame.draw.rect(tela, cor_borda, self.input_rect, 3, border_radius=10)

        cor_texto: Tuple[int, int, int] = Constantes.VERMELHO if self.nome_invalido else Constantes.COR_TEXTO
        nome_surf: pygame.Surface = self.fonte.render(self.nome, True, cor_texto)
        nome_rect = nome_surf.get_rect(midleft=(self.input_rect.x + 15, self.input_rect.centery))
        tela.blit(nome_surf, nome_rect)

        agora: int = pygame.time.get_ticks()
        if agora - self.cursor_timer > 500:
            self.cursor_visivel = not self.cursor_visivel
            self.cursor_timer = agora
        if self.cursor_visivel:
            cursor_x: int = nome_rect.right + 5
            pygame.draw.line(tela, cor_texto, (cursor_x, self.input_rect.y + 10),
                             (cursor_x, self.input_rect.y + self.input_rect.height - 10), 2)

        if self.nome_invalido:
            erro: pygame.Surface = self.fonte_pequena.render("Nome já existe! Tente outro.", True, Constantes.VERMELHO)
            erro_rect = erro.get_rect(center=(Constantes.LARGURA // 2, self.input_rect.bottom + 25))
            tela.blit(erro, erro_rect)

        instrucao: pygame.Surface = self.fonte_pequena.render("Pressione ENTER para confirmar ou ESC para voltar.", True, Constantes.BRANCO)
        instrucao_rect = instrucao.get_rect(center=(Constantes.LARGURA // 2, Constantes.ALTURA - 50))
        tela.blit(instrucao, instrucao_rect)