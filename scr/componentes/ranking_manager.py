import json
from typing import List, Dict, Union
from jogador_ranking import JogadorRanking 

class RankingManager:
    def __init__(self, nome_arquivo: str = "../assets/ranking/ranking_data.json") -> None: 
        self.nome_arquivo = nome_arquivo
        self.jogadores: List[JogadorRanking] = []
        self.carregar_de_arquivo()

    def carregar_de_arquivo(self) -> None:
        try:
            with open(self.nome_arquivo, 'r') as f:
                dados: List[Dict[str, Union[str, int]]] = json.load(f)
                self.jogadores = [JogadorRanking(j['nome'], j['pontuacao']) for j in dados]
        except (IOError, json.JSONDecodeError):
            self.jogadores = []
            print(f"Aviso: Arquivo de ranking '{self.nome_arquivo}' não encontrado ou inválido. Criando novo.")

    def adicionar_jogador(self, jogador: JogadorRanking) -> None:
        if not self.existe_nome(jogador.nome):
            self.jogadores.append(jogador)
            self.jogadores.sort(key=lambda x: x.pontuacao, reverse=True)
            self.salvar_em_arquivo()

    def salvar_em_arquivo(self) -> None:
        try:
            with open(self.nome_arquivo, 'w') as f:
                json.dump([j.to_dict() for j in self.jogadores], f, indent=4)
        except IOError as e:
            print(f"Erro ao salvar ranking: {e}")

    def existe_nome(self, nome: str) -> bool:
        """Verifica se um nome (ignorando maiúsculas/minúsculas) já existe."""
        return any(j.nome.lower() == nome.lower() for j in self.jogadores)
